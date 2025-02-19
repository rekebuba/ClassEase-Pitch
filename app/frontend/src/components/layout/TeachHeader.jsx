import {
    FaHome,
    FaCog,
    FaCogs,
    FaFileAlt,
    FaUserGraduate,
} from "react-icons/fa";
import classEaseHeader from '../../assets/images/ClassEase-header.png';
import { useNavigate } from "react-router-dom";

/**
 * TeacherHeader component renders the header section for the teacher's dashboard.
 * It includes navigation links to the dashboard, student management, and profile update pages.
 *
 * @component
 * @example
 * return (
 *   <TeacherHeader />
 * )
 *
 * @returns {JSX.Element} The rendered header component.
 *
 * @function
 * @name TeacherHeader
 *
 * @description
 * The TeacherHeader component provides navigation options for teachers to manage students,
 * access the dashboard, and update their profile. It uses the `useNavigate` hook from
 * `react-router-dom` to handle navigation.
 */
const TeacherHeader = () => {
    const navigate = useNavigate();

    /**
     * Navigates to the home page.
     *
     * @param {Event} e - The event object.
     */
    const goToHome = () => {
        navigate("/");
    };

    /**
     * @function manageStudents
     * @description Navigates to the student management page.
     */
    const manageStudents = () => {
        navigate("/teacher/students");
    };

    /**
     * @function goToDashboard
     * @description Navigates to the teacher's dashboard.
     */
    const goToDashboard = () => {
        navigate("/teacher/dashboard");
    };

    /**
     * @function updateProfile
     * @description Navigates to the profile update page.
     */
    const updateProfile = () => {
        navigate("/teacher/update/profile");
    };

    return (
        <header className="flex w-full p-2 bg-white shadow border-b border-gray-200 fixed">
            {/* Left Section: Logo */}
            <div className="cursor-pointer flex-shrink-0 align-middle" onClick={goToHome}>
                <img src={classEaseHeader} alt="ClassEase School" className="h-10" />
            </div>

            {/* Center Section: Navigation */}
            <div className="container mx-auto flex items-center justify-between py-4">
                <nav className="flex-1 flex justify-center space-x-6 items-center">
                    {/* Home Link */}
                    <div>
                        <span
                            onClick={goToDashboard}
                            className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer"
                        >
                            <FaHome className="h-5 w-5" />
                            <span>Home</span>
                        </span>
                    </div>

                    {/* Assessments & Exams Dropdown */}
                    <div className="relative group">
                        <span className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                            <FaFileAlt className="h-5 w-5" />
                            <span>Assessments & Exams</span>
                        </span>
                        <div className="absolute left-0 mt-2 w-48 bg-white shadow-lg rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10">
                            <div className="py-2">
                                <div
                                    onClick={manageStudents}
                                    className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-100 cursor-pointer"
                                >
                                    <FaUserGraduate className="h-5 w-5" />
                                    <span>My Students</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Settings Dropdown */}
                    <div className="relative group">
                        <span className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                            <FaCog className="h-5 w-5" />
                            <span>Settings</span>
                        </span>
                        <div className="absolute left-0 mt-2 w-48 bg-white shadow-lg rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10">
                            <div className="py-2">
                                <div
                                    onClick={updateProfile}
                                    className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-100 cursor-pointer"
                                >
                                    <FaCogs className="h-5 w-5" />
                                    <span>Update Profile</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Right Section: Empty filler to balance layout */}
                <div className="w-24"></div>
            </div>
        </header>
    );
};

export default TeacherHeader;
