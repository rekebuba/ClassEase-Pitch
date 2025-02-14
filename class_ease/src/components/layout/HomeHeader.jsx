import classEaseHeader from '../../assets/images/ClassEase-header.png';
import { useNavigate } from 'react-router-dom';

/**
 * HomeHeader component renders the header section of the homepage.
 * 
 * This component includes:
 * - A logo with the text "ClassEase School".
 * - A navigation bar with links to different sections of the site: Home, About Us, Admissions, Academics, and Contact.
 * - A login button that redirects to the login page.
 * 
 * @component
 * @example
 * return (
 *   <HomeHeader />
 * )
 */
function HomeHeader() {
    const navigate = useNavigate();

    const goToHome = () => {
        navigate("/");
    };

    return (
        <header className="flex items-center justify-between p-4 bg-white shadow-md">
            {/* Logo Section */}
            <div className="cursor-pointer" onClick={goToHome}>
                <img
                    src={classEaseHeader}
                    alt="ClassEase School"
                    className="h-12"
                />
            </div>
            {/* Navigation Links */}
            <nav>
                <ul className="flex space-x-8">
                    <li>
                        <a
                            href="#home"
                            className="text-gray-700 hover:text-blue-600 transition-colors"
                        >
                            Home
                        </a>
                    </li>
                    <li>
                        <a
                            href="#about"
                            className="text-gray-700 hover:text-blue-600 transition-colors"
                        >
                            About Us
                        </a>
                    </li>
                    <li>
                        <a
                            href="#academics"
                            className="text-gray-700 hover:text-blue-600 transition-colors"
                        >
                            Academics
                        </a>
                    </li>
                    <li>
                        <a
                            href="#contact"
                            className="text-gray-700 hover:text-blue-600 transition-colors"
                        >
                            Contact
                        </a>
                    </li>
                </ul>
            </nav>
            {/* Login Button */}
            <div>
                <a
                    href="/login"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md shadow hover:bg-blue-700 transition-colors"
                >
                    Login
                </a>
            </div>
        </header>
    );
}


export default HomeHeader;
