import React from 'react';
import classEaseHeader from '../images/ClassEase-header.png';
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

    return (<header className="header">
        <div className="header-logo" onClick={goToHome}>
            <img src={classEaseHeader} alt="ClassEase School" />
        </div>
        <nav>
            <ul className="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About Us</a></li>
                <li><a href="#academics">Academics</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
        <div className="login-btn">
            <a href="/login">Login</a>
        </div>
    </header>);
}


export default HomeHeader;
