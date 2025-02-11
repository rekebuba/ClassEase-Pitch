import {
    FaHome,
    FaUserGraduate,
    FaChalkboardTeacher,
    FaCog,
    FaCogs,
    FaChartBar,
    FaUsers,
    FaUserShield,
    FaBookOpen,
    FaUserPlus,
    FaFileAlt,
    FaBookReader,
    FaGraduationCap,
    FaChartPie,
    FaFileInvoice,
    FaFileContract,
    FaCalendarCheck,
    FaPlusCircle,
    FaEdit,
    FaRegCalendarAlt
} from "react-icons/fa";
import classEaseHeader from '../images/ClassEase-header.png';
import { useNavigate } from "react-router-dom";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
/**
 * AdminHeader component renders the header section of the admin dashboard.
 * It includes navigation links for various administrative tasks such as 
 * managing students and teachers, creating events, and accessing reports.
 * 
 * @component
 * @example
 * return (
 *   <AdminHeader />
 * )
 * 
 * @returns {JSX.Element} The rendered header component for the admin dashboard.
 * 
 * @function
 * @name AdminHeader
 * 
 * @description
 * The AdminHeader component provides a set of navigation links organized into 
 * dropdown menus. Each link triggers a navigation action to a different part 
 * of the admin interface. The component uses the `useNavigate` hook from 
 * `react-router-dom` to handle navigation.
 * 
 * @property {function} manageStudents - Navigates to the student management page.
 * @property {function} manageTeachers - Navigates to the teacher management page.
 * @property {function} assessMarkList - Navigates to the mark list assessment page.
 * @property {function} createEvent - Navigates to the new event creation page.
 * @property {function} goToDashboard - Navigates to the admin dashboard.
 * @property {function} userAccessControl - Navigates to the user access control page.
 * @property {function} enrollStudent - Navigates to the student enrollment page.
 * @property {function} enrollTeacher - Navigates to the teacher registration page.
 * @property {function} updateProfile - Navigates to the profile update page.
 */
const AdminHeader = () => {
    const navigate = useNavigate();

    const goToHome = () => {
        navigate("/");
    };

    const manageStudents = () => {
        navigate("/admin/manage/students");
    };

    const manageTeachers = () => {
        navigate("/admin/manage/teachers");
    };

    const assessMarkList = () => {
        navigate("/admin/assessment/marklist");
    };

    const createEvent = () => {
        navigate("/admin/events/newevent");
    };

    const goToDashboard = () => {
        navigate("/admin/dashboard");
    };

    const userAccessControl = () => {
        navigate("/admin/users/accesscontrol");
    };

    const enrollStudent = () => {
        navigate("/admin/student/registration");
    };

    const enrollTeacher = () => {
        navigate("/admin/teacher/registration");
    };

    const updateProfile = () => {
        navigate("/admin/update/profile");
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

                    <div>
                        <span
                            onClick={goToDashboard}
                            className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer"
                        >
                            <FaHome className="h-5 w-5" />
                            <span>Home</span>
                        </span>
                    </div>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaUsers className="h-5 w-5" />
                                <span>User Management</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={manageStudents}>
                                <FaUserGraduate className="h-5 w-5" />
                                <span>Manage Students</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={manageTeachers}>
                                <FaChalkboardTeacher className="h-5 w-5" />
                                <span>Manage Teachers</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={userAccessControl}>
                                <FaUserShield className="h-5 w-5" />
                                <span>Roles & Permissions</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaBookOpen className="h-5 w-5" />
                                <span>Registration</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={enrollStudent}>
                                <FaUserPlus className="h-5 w-5" />
                                <span>Enroll Students</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={enrollTeacher}>
                                <FaUserPlus className="h-5 w-5" />
                                <span>Register Teacher</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span
                                className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaFileAlt className="h-5 w-5" />
                                <span>Assessments & Exams</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={assessMarkList}>
                                <FaBookReader />
                                <span>Create Mark List</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <FaGraduationCap className="h-5 w-5" />
                                <span>Manage Final Exams</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span
                                className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaCalendarCheck className="h-5 w-5" />
                                <span>Events & Activities</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={createEvent}>
                                <FaPlusCircle />
                                <span>Create New Event</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <FaEdit className="h-5 w-5" />
                                <span>Manage Events</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <FaRegCalendarAlt className="h-5 w-5" />
                                <span>Event Calendar</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span
                                className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaChartBar className="h-5 w-5" />
                                <span>Report</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={createEvent}>
                                <FaChartPie />
                                <span>Student Performance Report</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <FaFileInvoice className="h-5 w-5" />
                                <span>Attendance Reports</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <FaFileContract className="h-5 w-5" />
                                <span>Exam Reports</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <span
                                className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer">
                                <FaCog className="h-5 w-5" />
                                <span>Settings</span>
                            </span>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-48">
                            <DropdownMenuItem onClick={updateProfile}>
                                <FaCogs className="h-5 w-5" />
                                <span>Update Profile</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </nav>
            </div >
        </header >
    );
};

export default AdminHeader;
