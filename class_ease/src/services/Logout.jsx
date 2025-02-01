import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

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

    useEffect(() => {
        // Clear tokens from local storage
        localStorage.removeItem('Authorization');

        // Redirect to the login page
        navigate('/login');
    }, [navigate]);

    return null;
};

export default Logout;
