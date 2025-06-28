from datetime import datetime
import random
from typing import Any, Dict, List, Optional
import bcrypt
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from pyethiodate import EthDate  # type: ignore

from extension.enums.enum import GradeLevelEnum, RoleEnum

from models.user import User
from models import storage


class DetailApplicationResponse(BaseModel):
    model_config = dict(populate_by_name=True, from_attributes=True)

    subjects_to_teach: List[str]
    grade_levels_to_teach: List[GradeLevelEnum]


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identification: Optional[str]
    password: Optional[str] = Field(exclude=True)
    role: RoleEnum
    national_id: str
    image_path: Optional[str] = None

    # Hash password before validation
    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, v: str) -> Optional[str]:
        return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Set both identification and password in one place
    @model_validator(mode="before")
    @classmethod
    def generate_id_and_password(self, data: Dict[str, Any]) -> Dict[str, Any]:
        role = data.get("role")
        if not role:
            raise ValueError("Role must be provided")

        role_prefix_map = {
            RoleEnum.STUDENT: "MAS",
            RoleEnum.TEACHER: "MAT",
            RoleEnum.ADMIN: "MAA",
        }
        section = role_prefix_map[role]

        # Only generate if not provided
        if not data.get("identification") or not data.get("password"):
            while True:
                num = random.randint(1000, 9999)
                year_suffix = EthDate.date_to_ethiopian(datetime.now()).year % 100
                generated_id = f"{section}/{num}/{year_suffix}"
                if not storage.get_first(User, identification=generated_id):
                    data["identification"] = generated_id
                    data["password"] = generated_id
                    break
        return data

    # Validate uniqueness of national_id
    @model_validator(mode="after")
    def check_user_exists(self) -> "UserCreateSchema":
        if (
            storage.session.query(User.id)
            .filter_by(national_id=self.national_id)
            .scalar()
        ):
            raise ValueError("User already exists.")
        return self
