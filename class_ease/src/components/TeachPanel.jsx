import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import api from '../services/api';


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
                const response = await api.get('/teacher/dashboard');
                setTeacherData(response.data);
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    console.error(error.response.data['error']);
                }
                return;
            }
        };
        fetchAdmin();
    }, []);

    /**
     * @function handleLogout
     * @description Navigates to the logout page.
     */
    const handleLogout = () => {
        navigate('/logout');
    };

    return (
        <aside className="flex flex-col justify-between bg-white p-6 border-r border-gray-200">
            {/* Top Profile Section */}
            <div className="flex flex-col items-center space-y-4">
                <FaUserCircle className="w-16 h-16 text-gray-500" />
                <h3 className="mt-4 text-xl font-semibold text-gray-800">
                    {teacherData.__class__} Panel
                </h3>
                <p className="text-sm text-gray-600">
                    Mr. {teacherData.first_name} {teacherData.last_name}
                </p>
            </div>
            {/* Bottom Navigation Section */}
            <nav className="menu">
                <ul>
                    <li
                        onClick={handleLogout}
                        className="flex items-center space-x-2 cursor-pointer text-gray-700 hover:text-red-600 transition-colors"
                    >
                        <FaSignOutAlt className="w-5 h-5" />
                        <span>Logout</span>
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default TeacherPanel;
