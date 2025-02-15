import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt } from "react-icons/fa";
import { AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader, AlertDialogFooter, AlertDialogTitle, AlertDialogDescription, AlertDialogCancel, AlertDialogAction } from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { authApi } from "@/api";

/**
 * Logout component that handles user logout functionality.
 *
 * This component performs the following actions:
 * - Clears the 'Authorization' token from local storage.
 * - Redirects the user to the login page.
 *
 * @component
 * @example
 * // Usage example:
 * // <Logout />
 *
 * @returns {null} This component does not render any UI.
 */
const Logout = () => {
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);

    const handleLogout = async () => {
        setOpen(false);
        try {
            const response = await authApi.logout();
            localStorage.removeItem('Authorization'); // Clear tokens from local storage
            navigate('/login');
            toast.success(response.data['message'], {
                description: currentTime,
                style: { color: 'green' }
            });
        } catch (error) {
            console.log(error.response.data)
            if (error.response && error.response.data && error.response.data['error']) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            } else {
                toast.error("An unexpected error occurred.", {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
    };

    return (
        <AlertDialog open={open} onOpenChange={setOpen}>
            <AlertDialogTrigger asChild>
                <Button
                    className="align-bottom space-x-2 mb-20 cursor-pointer bg-transparent hover:bg-transparent text-gray-700 hover:text-red-600 hover:scale-105 text-xl"
                >
                    <FaSignOutAlt className="w-5 h-5" /> Logout
                </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle className="text-left">Are you absolutely sure?</AlertDialogTitle>
                    <AlertDialogDescription>
                        This will log you out of your account. You will need to log in again to access your data.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={handleLogout}>LogOut</AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
};

export default Logout;
