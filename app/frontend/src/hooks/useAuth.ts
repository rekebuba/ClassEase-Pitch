import { useEffect, useState } from 'react';

const useAuth = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userRole, setUserRole] = useState(null);
    const [loading, setLoading] = useState(true); // Add a loading state

    useEffect(() => {
        // Check if a token exists in localStorage
        const token = localStorage.getItem('apiKey');
        if (token) {
            setIsAuthenticated(true);

            // Decode the token to get the user's role (if applicable)
            const decodedToken = decodeToken(token); // Implement this function
            if (decodedToken && decodedToken.role) {
                setUserRole(decodedToken.role);
            }
        } else {
            setIsAuthenticated(false);
            setUserRole(null);
        }

        setLoading(false); // Set loading to false after checking the token
    }, []);

    return { isAuthenticated, userRole, loading };
};

// Helper function to decode the JWT token
const decodeToken = (token) => {
    try {
        // JWT tokens are in the format: header.payload.signature
        const payload = token.split('.')[1]; // Get the payload part
        const decodedPayload = atob(payload); // Decode base64
        return JSON.parse(decodedPayload); // Parse the JSON payload
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
};

export default useAuth;
