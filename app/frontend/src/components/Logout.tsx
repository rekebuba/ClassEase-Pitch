"use client";

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader, AlertDialogFooter, AlertDialogTitle, AlertDialogDescription, AlertDialogCancel, AlertDialogAction } from "@/components/ui/alert-dialog";
import { toast } from "sonner";
import { authApi, zodApiHandler } from "@/api";
import { LogOut } from "lucide-react"
import { logoutSchema } from '@/lib/validations';

/**
 * Logout component that handles user logout functionality.
 *
 * This component performs the following actions:
 * - Clears the 'apiKey' token from local storage.
 * - Redirects the user to the login page.
 */
const Logout = () => {
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);

    const handleLogout = async () => {
        setOpen(false);
        const result = await zodApiHandler(
            () => authApi.logout(),
            logoutSchema
        );
        if (!result.success) {
            toast.error(result.error.message, {
                description: "Please try again later, if the problem persists, contact the administrator.",
                style: { color: 'red' }
            });
            return;
        }

        localStorage.removeItem('apiKey'); // Clear tokens from local storage
        navigate('/auth');
        toast.success(result.data.message, {
            style: { color: 'green' }
        });
    };

    return (
        <AlertDialog open={open} onOpenChange={setOpen}>
            <AlertDialogTrigger asChild>
                <div className='flex gap-2'>
                    <LogOut />
                    Log out
                </div>
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
