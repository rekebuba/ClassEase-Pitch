import logging
from datetime import datetime, timezone
from typing import Annotated, Any, Dict, Optional

import jwt
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from pydantic import NameEmail
from sqlalchemy import select

from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    MembershipSelectionRequest,
    MembershipSummary,
    MessageResponse,
    OTPRequest,
    PasswordRecovery,
    PasswordResetRequest,
    ProviderResponse,
    RefreshTokenRequest,
    SchoolSummary,
    VerifyOTPResponse,
)
from project.api.v1.routers.auth.service import (
    get_google_user,
    send_reset_password_email,
    verify_email_verification_token,
    verify_otp_and_generate_token,
    verify_password_reset_token,
)
from project.api.v1.routers.dependencies import (
    AuthenticatedActor,
    RedisDep,
    SessionDep,
    TokenDep,
    get_current_actor,
)
from project.api.v1.routers.schema import HTTPError
from project.core.access_control import (
    create_auth_session,
    generate_refresh_token,
    get_membership_with_roles,
    hash_refresh_token,
    load_user_memberships_by_identifier,
    load_user_memberships_for_user,
    record_audit_log,
    resolve_membership_permissions,
    resolve_membership_role_names,
    resolve_shell_role_from_names,
)
from project.core.config import settings
from project.core.security import (
    ALGORITHM,
    check_password,
    create_access_token,
    get_password_hash,
)
from project.core.tenant import get_request_school_slug
from project.models import (
    AuthIdentity,
    AuthSession,
    BlacklistToken,
    SchoolMembership,
    User,
)
from project.utils.enum import (
    AuthProviderEnum,
    AuthSessionAssuranceEnum,
    SchoolMembershipStatusEnum,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


class SchoolAwareOAuth2PasswordRequestForm:
    def __init__(
        self,
        *,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        school_slug: Annotated[Optional[str], Form(alias="schoolSlug")] = None,
        grant_type: Annotated[Optional[str], Form()] = None,
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[Optional[str], Form()] = None,
        client_secret: Annotated[Optional[str], Form()] = None,
    ) -> None:
        self.username = username
        self.password = password
        self.school_slug = school_slug
        self.grant_type = grant_type
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret


def _parse_school_aware_identifier(
    identifier: str,
    explicit_school_slug: str | None,
) -> tuple[str, str | None]:
    if explicit_school_slug:
        return identifier.strip(), explicit_school_slug.strip().lower()

    value = identifier.strip()
    if ":" not in value:
        return value, None

    school_slug, login_identifier = value.split(":", 1)
    return login_identifier.strip(), school_slug.strip().lower()


def _build_school_summary(membership: SchoolMembership) -> SchoolSummary:
    school = membership.school
    return SchoolSummary(
        id=school.id,
        name=school.name,
        slug=school.slug,
        status=school.status,
    )


def _build_membership_summary(membership: SchoolMembership) -> MembershipSummary:
    role_names = sorted(resolve_membership_role_names(membership))
    permissions = sorted(resolve_membership_permissions(membership))
    shell_role = resolve_shell_role_from_names(
        role_names, fallback=membership.user.role
    )
    return MembershipSummary(
        id=membership.id,
        school_id=membership.school_id,
        school_slug=membership.school.slug,
        school_name=membership.school.name,
        status=membership.status,
        login_identifier=membership.login_identifier,
        is_primary=membership.is_primary,
        role_names=role_names,
        shell_role=shell_role,
        permissions=permissions,
    )


def _pick_single_membership(
    memberships: list[SchoolMembership],
    *,
    school_slug: str | None,
) -> SchoolMembership:
    if not memberships:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if len(memberships) > 1 and school_slug is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple school memberships found. \
                Provide school context to continue.",
        )

    return memberships[0]


async def _issue_school_scoped_tokens(
    session: SessionDep,
    *,
    user: User,
    membership: SchoolMembership,
    assurance_level: AuthSessionAssuranceEnum,
    request: Request,
) -> LoginTokenResponse:
    refresh_token = generate_refresh_token()
    auth_session = await create_auth_session(
        session,
        user=user,
        membership=membership,
        refresh_token=refresh_token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
        assurance_level=assurance_level,
    )

    role_names = resolve_membership_role_names(membership)
    permissions = resolve_membership_permissions(membership)
    shell_role = resolve_shell_role_from_names(role_names, fallback=user.role)

    access_token = create_access_token(
        subject=str(user.id),
        role=shell_role,
        school_id=str(membership.school_id),
        school_slug=membership.school.slug,
        membership_id=str(membership.id),
        session_id=str(auth_session.id),
        permissions_version=membership.permissions_version,
        permissions=permissions,
        mfa_state=membership.mfa_state.value,
    )

    available_memberships = [
        _build_membership_summary(item)
        for item in await load_user_memberships_for_user(session, user_id=user.id)
    ]

    await record_audit_log(
        session,
        action="auth.login",
        outcome="success",
        school_id=membership.school_id,
        user_id=user.id,
        membership_id=membership.id,
        auth_session_id=auth_session.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details={"schoolSlug": membership.school.slug, "role": shell_role.value},
    )
    await session.commit()

    return LoginTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        active_school=_build_school_summary(membership),
        active_membership=_build_membership_summary(membership),
        available_memberships=available_memberships,
    )


@router.post(
    "/login",
    response_model=LoginTokenResponse,
    operation_id="login_credential",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Incorrect Credential",
        },
    },
)
async def login(
    request: Request,
    form_data: Annotated[SchoolAwareOAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginTokenResponse:
    login_identifier, school_slug = _parse_school_aware_identifier(
        form_data.username,
        form_data.school_slug or get_request_school_slug(),
    )
    memberships = list(
        await load_user_memberships_by_identifier(
            session,
            identifier=login_identifier,
            school_slug=school_slug,
        )
    )
    membership = _pick_single_membership(memberships, school_slug=school_slug)
    user = membership.user

    identity = next(
        (
            auth_identity
            for auth_identity in user.auth_identities
            if auth_identity.provider == AuthProviderEnum.PASSWORD
        ),
        None,
    )

    if (
        identity is None
        or identity.password is None
        or not check_password(form_data.password, identity.password)
    ):
        logger.warning("Failed password attempt for user %s", user.id)
        await record_audit_log(
            session,
            action="auth.login",
            outcome="failure",
            school_id=membership.school_id,
            user_id=user.id,
            membership_id=membership.id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            details={"reason": "invalid_credentials"},
        )
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active or membership.status != SchoolMembershipStatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This school membership is inactive.",
        )

    return await _issue_school_scoped_tokens(
        session,
        user=user,
        membership=membership,
        assurance_level=AuthSessionAssuranceEnum.PASSWORD_ONLY,
        request=request,
    )


@router.post(
    "/login/{provider}",
    status_code=status.HTTP_200_OK,
    response_model=LoginTokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid Google token or user not found",
        },
    },
)
async def login_provider(
    provider: AuthProviderEnum,
    data: ProviderResponse,
    request: Request,
    session: SessionDep,
) -> LoginTokenResponse:
    if data.credential is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credential is required for provider login",
        )

    provider_handlers = {
        provider.GOOGLE: get_google_user,
    }
    user = await provider_handlers[provider](session, data.credential)

    school_slug = data.school_slug or get_request_school_slug()
    memberships = list(
        await load_user_memberships_for_user(
            session,
            user_id=user.id,
            school_slug=school_slug,
        )
    )
    membership = _pick_single_membership(memberships, school_slug=school_slug)

    return await _issue_school_scoped_tokens(
        session,
        user=user,
        membership=membership,
        assurance_level=AuthSessionAssuranceEnum.FEDERATED,
        request=request,
    )


@router.post(
    "/refresh",
    response_model=LoginTokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid refresh token",
        },
    },
)
async def refresh_access_token(
    request: RefreshTokenRequest,
    session: SessionDep,
) -> LoginTokenResponse:
    auth_session = (
        await session.execute(
            select(AuthSession).where(
                AuthSession.refresh_token_hash
                == hash_refresh_token(request.refresh_token)
            )
        )
    ).scalar_one_or_none()

    if (
        auth_session is None
        or auth_session.revoked_at is not None
        or auth_session.expires_at <= datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    membership = await get_membership_with_roles(session, auth_session.membership_id)
    if membership is None or membership.status != SchoolMembershipStatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = membership.user
    refresh_token = generate_refresh_token()
    auth_session.refresh_token_hash = hash_refresh_token(refresh_token)
    auth_session.last_seen_at = datetime.now(timezone.utc)

    role_names = resolve_membership_role_names(membership)
    permissions = resolve_membership_permissions(membership)
    shell_role = resolve_shell_role_from_names(role_names, fallback=user.role)
    access_token = create_access_token(
        subject=str(user.id),
        role=shell_role,
        school_id=str(membership.school_id),
        school_slug=membership.school.slug,
        membership_id=str(membership.id),
        session_id=str(auth_session.id),
        permissions_version=membership.permissions_version,
        permissions=permissions,
        mfa_state=membership.mfa_state.value,
    )

    await record_audit_log(
        session,
        action="auth.refresh",
        outcome="success",
        school_id=membership.school_id,
        user_id=user.id,
        membership_id=membership.id,
        auth_session_id=auth_session.id,
    )
    await session.commit()

    return LoginTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        active_school=_build_school_summary(membership),
        active_membership=_build_membership_summary(membership),
        available_memberships=[
            _build_membership_summary(item)
            for item in await load_user_memberships_for_user(session, user_id=user.id)
        ],
    )


@router.post(
    "/select-membership",
    response_model=LoginTokenResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "Membership not found",
        },
    },
)
async def select_membership(
    request_data: MembershipSelectionRequest,
    request: Request,
    session: SessionDep,
    token: TokenDep,
    current_actor: Annotated[AuthenticatedActor, Depends(get_current_actor)],
) -> LoginTokenResponse:
    target_membership = await get_membership_with_roles(
        session, request_data.membership_id
    )
    if (
        target_membership is None
        or target_membership.user_id != current_actor.user.id
        or target_membership.status != SchoolMembershipStatusEnum.ACTIVE
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    current_actor.auth_session.revoked_at = datetime.now(timezone.utc)
    current_actor.auth_session.revoke_reason = "school_switch"

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
        jti = payload.get("jti")
        if isinstance(jti, str):
            session.add(BlacklistToken(jti=jti))
    except jwt.PyJWTError:
        logger.warning("Unable to blacklist access token during school switch.")

    await record_audit_log(
        session,
        action="auth.switch_school",
        outcome="success",
        school_id=target_membership.school_id,
        user_id=current_actor.user.id,
        membership_id=target_membership.id,
        auth_session_id=current_actor.auth_session.id,
        details={"fromMembershipId": str(current_actor.membership.id)},
    )

    refresh_token = generate_refresh_token()
    new_session = await create_auth_session(
        session,
        user=current_actor.user,
        membership=target_membership,
        refresh_token=refresh_token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
        assurance_level=current_actor.auth_session.assurance_level,
    )

    role_names = resolve_membership_role_names(target_membership)
    permissions = resolve_membership_permissions(target_membership)
    shell_role = resolve_shell_role_from_names(
        role_names, fallback=current_actor.user.role
    )
    access_token = create_access_token(
        subject=str(current_actor.user.id),
        role=shell_role,
        school_id=str(target_membership.school_id),
        school_slug=target_membership.school.slug,
        membership_id=str(target_membership.id),
        session_id=str(new_session.id),
        permissions_version=target_membership.permissions_version,
        permissions=permissions,
        mfa_state=target_membership.mfa_state.value,
    )

    await session.commit()

    return LoginTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        active_school=_build_school_summary(target_membership),
        active_membership=_build_membership_summary(target_membership),
        available_memberships=[
            _build_membership_summary(item)
            for item in await load_user_memberships_for_user(
                session,
                user_id=current_actor.user.id,
            )
        ],
    )


@router.get(
    "/verify-email",
    response_model=MessageResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid or expired token",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "User not found",
        },
    },
)
async def verify_email(
    session: SessionDep,
    token: str,
) -> MessageResponse:
    """Endpoint to verify a user's email using a token."""
    email = verify_email_verification_token(
        token, settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS
    )
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = (
        await session.execute(select(User).filter(User.email == email))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_verified = True
    await session.commit()

    return MessageResponse(message="Email successfully verified")


@router.post(
    "/logout",
    response_model=MessageResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid token format",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid token",
        },
    },
)
async def logout(
    token: TokenDep,
    session: SessionDep,
) -> Dict[str, Any]:
    """
    Endpoint to log out a user by blacklisting their JWT token and revoking the session.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
        jti = payload.get("jti")
        session_id = payload.get("session_id")

        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token format"
            )

        existing_blacklist = (
            await session.execute(
                select(BlacklistToken).filter(BlacklistToken.jti == jti)
            )
        ).scalar_one_or_none()
        if existing_blacklist:
            return {"message": "Token was already invalidated"}

        if session_id is not None:
            auth_session = await session.get(AuthSession, session_id)
            if auth_session is not None and auth_session.revoked_at is None:
                auth_session.revoked_at = datetime.now(timezone.utc)
                auth_session.revoke_reason = "logout"

        session.add(BlacklistToken(jti=jti))
        await session.commit()

        return {"message": "Successfully logged out"}

    except jwt.PyJWTError as e:
        logger.error("Token validation error during logout: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


@router.post(
    "/password-recovery",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "User not found",
        },
    },
)
async def password_recovery(
    data: PasswordRecovery,
    session: SessionDep,
    redis: RedisDep,
) -> MessageResponse:
    """Endpoint to initiate password recovery by sending an OTP to the user's email."""
    user = (
        await session.execute(select(User).filter(User.email == data.email))
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await send_reset_password_email(NameEmail(email=data.email, name=data.email), redis)
    return MessageResponse(message="Password recovery email sent")


@router.post(
    "/verify-otp",
    status_code=status.HTTP_200_OK,
    response_model=VerifyOTPResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid or expired OTP",
        },
    },
)
async def verify_otp(otp_request: OTPRequest, redis: RedisDep) -> VerifyOTPResponse:
    """Endpoint to verify the OTP sent to the user's email for password recovery."""
    is_valid_with_token = await verify_otp_and_generate_token(
        email=otp_request.email, user_submitted_code=otp_request.otp, redis_client=redis
    )

    if not is_valid_with_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    return VerifyOTPResponse(
        message="OTP verified successfully", token=is_valid_with_token
    )


@router.post(
    "/password-reset",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid or expired token",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "User not found",
        },
    },
)
async def password_reset(
    request: PasswordResetRequest,
    session: SessionDep,
    redis: RedisDep,
) -> MessageResponse:
    """Endpoint to reset the user's password using a valid token."""
    is_verified = await verify_password_reset_token(request.email, request.token, redis)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = (
        (await session.execute(select(User).filter(User.email == request.email)))
        .scalars()
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    identity = (
        (
            await session.execute(
                select(AuthIdentity).filter_by(
                    user_id=user.id,
                    provider=AuthProviderEnum.PASSWORD,
                )
            )
        )
        .scalars()
        .first()
    )
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password authentication method not found for user",
        )

    identity.password = get_password_hash(request.new_password)
    await session.commit()

    return MessageResponse(message="Password successfully reset")
