import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

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
