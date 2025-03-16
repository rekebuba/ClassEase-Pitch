import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";
import { teacherApi } from '@/api';
import { Logout } from "@/features/auth";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

/**
 * TeacherPanel component renders the sidebar for the teacher's dashboard.
 * It fetches teacher data from the API and displays the teacher's profile information.
 * 
 * @component
 * 
 * @example
 * return (
 *   <TeacherPanel />
 * )
 * 
 * @returns {JSX.Element} The rendered sidebar component for the teacher's dashboard.
 * 
 * @function
 * @name TeacherPanel
 * 
 * @description
 * This component uses the `useNavigate` hook from `react-router-dom` for navigation and 
 * the `useState` and `useEffect` hooks from `react` to manage state and side effects.
 * It fetches teacher data from the `/teacher/dashboard` endpoint and displays the teacher's 
 * profile information including their name, class, and subject taught. It also provides a 
 * logout option that navigates to the logout page.
 */
const TeacherPanel = () => {
    const navigate = useNavigate();
    const [teacherData, setTeacherData] = useState({});
    const [previewImage, setPreviewImage] = useState('');

    /**
     * @hook useEffect
     * @description Fetches teacher data from the API when the component mounts.
     */
    useEffect(() => {
        /**
         * @async
         * @function fetchAdmin
         * @description Fetches teacher data from the API and updates the state.
         * @throws Will log an error message to the console if the API request fails.
         * @returns {undefined} Returns early if there is an error.
         * @param {Object} error - The error response from the API.
         * @param {Object} error.response - The response object from the API.
         * @param {Object} error.response.data - The data object from the API response.
         * @param {string} error.response.data['error'] - The error message from the API response.
         */
        const fetchAdmin = async () => {
            try {
                const response = await teacherApi.getPanelData();
                const flattenedData = {
                    ...response.data['user'],
                    ...response.data['teacher'],
                };
                setTeacherData(flattenedData);
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
        navigate("/teacher/update/profile");
    };

    return (
        <aside className="flex flex-col justify-between fixed mt-[4.6rem] h-full w-48 bg-white p-7 border-r border-gray-200">
            {/* Top Profile Section */}
            <div className="flex flex-col items-center space-y-4">
                <Avatar className="w-16 h-16 cursor-pointer" onClick={updateProfile}>
                    <AvatarImage src={teacherData.imageUrl} />
                    <AvatarFallback><FaUserCircle className="w-16 h-16 text-gray-500 cursor-pointer" /></AvatarFallback>
                </Avatar>
                <h3 className="mt-4 text-center text-xl font-semibold text-gray-800">
                    Teacher Panel
                </h3>
                <p className="text-sm text-gray-600 text-wrap text-center font-semibold">
                    Mr. {teacherData.firstName} {teacherData.fatherName} {teacherData.grandFatherName}
                </p>
            </div>
            <Logout />
        </aside>
    );
};

export default TeacherPanel;
