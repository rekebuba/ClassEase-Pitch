import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { Loader2Icon } from "lucide-react";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import { selectMembershipMutation } from "@/client/@tanstack/react-query.gen";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { loginFailure, loginSuccess } from "@/store/slice/auth-slice";
import { decodeToken } from "@/utils/utils";

import LoginTab from "./tab/login-tab";

import type {
  LoginResponse,
  MembershipSummary,
  SelectMembershipError,
} from "@/client/types.gen";
import type { AxiosError } from "axios";

type PendingMembershipState = {
  accessToken: string;
  memberships: MembershipSummary[];
};

function AuthActionBar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [pendingMembership, setPendingMembership] = useState<PendingMembershipState | null>(null);
  const [selectedMembershipId, setSelectedMembershipId] = useState("");

  const resolveRouteByRole = (role: string) => {
    if (role === "admin" || role === "student") {
      return `/${role}`;
    }
    return "/";
  };

  const finalizeAuthentication = (response: LoginResponse) => {
    const decodedToken = decodeToken(response.accessToken);

    if (!decodedToken) {
      dispatch(loginFailure("Invalid token received"));
      toast.error("Invalid token received", {
        style: { color: "red" },
      });
      return;
    }

    dispatch(
      loginSuccess({
        token: response.accessToken,
        refreshToken: response.refreshToken,
        userInfo: decodedToken,
        activeSchool: response.activeSchool ?? null,
        activeMembership: response.activeMembership ?? null,
        availableMemberships: response.availableMemberships ?? [],
      }),
    );

    const role = response.activeMembership?.shellRole || decodedToken.role;
    navigate({ to: resolveRouteByRole(role) });
  };

  const membershipMutation = useMutation({
    ...selectMembershipMutation(),
    onSuccess: (response) => {
      setPendingMembership(null);
      setSelectedMembershipId("");
      finalizeAuthentication(response);
    },
    onError: (error: AxiosError<SelectMembershipError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        toast.error(detail, {
          style: { color: "red" },
        });
        return;
      }
      toast.error("Failed to select membership. Please try again.", {
        style: { color: "red" },
      });
    },
  });

  const requestMembershipSelection = (
    loginResponse: LoginResponse,
    membershipId: string,
  ) => {
    membershipMutation.mutate({
      body: { membership_id: membershipId },
      headers: {
        Authorization: `Bearer ${loginResponse.accessToken}`,
      },
    });
  };

  const handleAuthResponse = (response: LoginResponse) => {
    const memberships = response.availableMemberships ?? [];
    const hasActiveMembership = !!response.activeMembership;

    if (!hasActiveMembership && memberships.length === 1) {
      requestMembershipSelection(response, memberships[0].id);
      return;
    }

    if (!hasActiveMembership && memberships.length > 1) {
      setPendingMembership({
        accessToken: response.accessToken,
        memberships,
      });
      setSelectedMembershipId(memberships[0].id);
      toast.info("Select your membership to continue.");
      return;
    }

    finalizeAuthentication(response);
  };

  const handleMembershipContinue = () => {
    if (!pendingMembership || !selectedMembershipId) {
      return;
    }

    membershipMutation.mutate({
      body: { membership_id: selectedMembershipId },
      headers: {
        Authorization: `Bearer ${pendingMembership.accessToken}`,
      },
    });
  };

  if (!pendingMembership) {
    return <LoginTab onAuthResponse={handleAuthResponse} />;
  }

  return (
    <Card className="border-0 shadow-lg animate-fade-left">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center">
          Select Membership
        </CardTitle>
        <CardDescription className="text-center">
          Your account has access to multiple schools or roles.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <FieldGroup>
          <Field>
            <FieldLabel htmlFor="membership">Membership</FieldLabel>
            <Select
              value={selectedMembershipId}
              onValueChange={setSelectedMembershipId}
            >
              <SelectTrigger id="membership">
                <SelectValue placeholder="Select a membership" />
              </SelectTrigger>
              <SelectContent>
                {pendingMembership.memberships.map(membership => (
                  <SelectItem key={membership.id} value={membership.id}>
                    {membership.schoolName}
                    {" - "}
                    {membership.shellRole}
                    {membership.loginIdentifier
                      ? ` (${membership.loginIdentifier})`
                      : ""}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>
        </FieldGroup>
      </CardContent>
      <CardFooter className="flex gap-2 justify-end">
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setPendingMembership(null);
            setSelectedMembershipId("");
          }}
        >
          Back
        </Button>
        <Button
          type="button"
          onClick={handleMembershipContinue}
          disabled={!selectedMembershipId || membershipMutation.isPending}
        >
          {membershipMutation.isPending && (
            <Loader2Icon className="animate-spin" />
          )}
          Continue
        </Button>
      </CardFooter>
    </Card>
  );
}

export default AuthActionBar;
