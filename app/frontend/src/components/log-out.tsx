import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { LogOut } from "lucide-react";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import { logoutMutation } from "@/client/@tanstack/react-query.gen";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { logout } from "@/store/slice/auth-slice";

import type { LogoutError } from "@/client/types.gen";
import type { AxiosError } from "axios";

/**
 * Logout component that handles user logout functionality.
 *
 * This component performs the following actions:
 * - Clears the 'apiKey' token from local storage.
 * - Redirects the user to the login page.
 */
function Logout() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const dispatch = useDispatch();

  const mutation = useMutation({
    ...logoutMutation(),
    onSuccess: (response) => {
      // removes token from redux
      dispatch(logout());

      // redirect after success
      navigate({ to: "/authentication" });
      toast.success(response.message, {
        style: { color: "green" },
      });
    },
    onError: (error: AxiosError<LogoutError>) => {
      const err = error.response?.data?.detail;
      if (err) {
        toast.error(err, {
          style: { color: "red" },
        });
      }
      toast.error("Something went wrong. Failed to Logout.", {
        style: { color: "red" },
      });
    },
  });

  const handleLogout = async () => {
    setOpen(false);
    mutation.mutate({});
  };

  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogTrigger asChild>
        <div className="flex gap-2">
          <LogOut />
          Log out
        </div>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle className="text-left">
            Are you absolutely sure?
          </AlertDialogTitle>
          <AlertDialogDescription>
            This will log you out of your account. You will need to log in again
            to access your data.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={handleLogout}>LogOut</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default Logout;
