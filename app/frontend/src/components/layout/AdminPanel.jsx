import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";
import { Logout } from "@/features/auth";
import { adminApi } from '@/api';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
/**
 * AdminPanel component renders the admin dashboard sidebar.
 * It fetches admin data from the server and displays the admin's profile information.
 * It also provides a logout option.
 *
 * @component
 * @example
 * return (
 *   <AdminPanel />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @function
 * @name AdminPanel
 *
 * @description
 * - Uses `useNavigate` from `react-router-dom` to navigate to the logout page.
 * - Uses `useState` to manage the admin data state.
 * - Uses `useEffect` to fetch admin data from the server when the component mounts.
 * - Displays the admin's profile information including name and role.
 * - Provides a logout option that navigates to the logout page.
 *
 * @dependencies
 * - `react`
 * - `react-router-dom`
 * - `react-icons/fa`
 * - `api` (assumed to be an instance of Axios or similar for making HTTP requests)
 */
const AdminPanel = () => {
    const navigate = useNavigate();
    const [adminData, setAdminData] = useState({});

    /**
     * @hook useEffect
     * @description Fetches admin data from the server when the component mounts.
     * @param {Function} fetchAdmin - Fetches admin data from the server.
     */
    useEffect(() => {
        const fetchAdmin = async () => {
            try {
                const response = await adminApi.getPanelData();
                const flattenedData = {
                    ...response.data['user'],
                    ...response.data['admin'],
                };
                setAdminData(flattenedData);
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    console.error(error.response.data['error']);
                }
                return;
            }
        };
        fetchAdmin();
    }, []);

    const updateProfile = () => {
        navigate("/admin/update/profile");
    };

    return (
        <aside className="flex flex-col justify-between fixed mt-[4.6rem] h-full w-48 bg-white p-7 border-r border-gray-200">
            <div className="flex flex-col items-center space-y-4">
                <Avatar className="w-16 h-16 cursor-pointer" onClick={updateProfile}>
                    <AvatarImage src={adminData.imageUrl} />
                    <AvatarFallback><FaUserCircle className="w-16 h-16 text-gray-500 cursor-pointer" /></AvatarFallback>
                </Avatar>
                <h3 className="mt-4 text-xl font-semibold text-gray-800">{adminData.role} Panel</h3>
                <p className="text-sm text-gray-600 text-wrap text-center font-bold">Mr. {adminData.firstName} {adminData.fatherName} {adminData.grandFatherName} </p>
                <p className="text-sm text-gray-600 text-wrap text-center font-bold">Principal</p>
            </div>
            <Logout />
        </aside>
    );
};

export default AdminPanel;
