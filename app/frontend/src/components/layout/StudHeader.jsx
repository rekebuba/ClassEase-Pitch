import { useNavigate } from "react-router-dom";
import classEaseHeader from '../../assets/images/ClassEase-header.png';
import {
    FaHome,
    FaFileAlt,
} from "react-icons/fa";

function StudentHeader() {
    const navigate = useNavigate();

    /**
    * Navigates the user to the home page.
    */
    const goToHome = () => {
        navigate("/");
    };

    /**
     * @function goToDashboard
     * @description Navigates to the teacher's dashboard.
     */
    const goToDashboard = () => {
        navigate("/student/dashboard");
    };


    const goToCourseRegistration = () => {
        navigate("/student/course/registration")
    };

    return (
        <header className="flex w-full h-[4.6rem] p-2 bg-white shadow border-b border-gray-200 fixed">
            <div className="cursor-pointer flex justify-between flex-shrink-0 align-middle" onClick={goToHome}>
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

                    {/* Course Registration Dropdown */}
                    <div className="relative group">
                        <span
                            onClick={goToCourseRegistration}
                            className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 cursor-pointer"
                        >
                            <FaFileAlt className="h-5 w-5" />
                            <span>Course Registration</span>
                        </span>
                    </div>
                </nav>

                {/* Right Section: Empty filler to balance layout */}
                <div className="w-24"></div>
            </div>
        </header>
    );
}

export default StudentHeader;
