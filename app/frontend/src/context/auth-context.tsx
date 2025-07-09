import { RoleEnumType } from '@/lib/enums';
import { jwtPayloadSchema, JwtPayloadType } from '@/lib/validations';
import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


interface AuthContextType {
    isAuthenticated: boolean;
    userId: string | null;
    userRole: RoleEnumType | null;
    isLoading: boolean;
    login: (token: string, role: RoleEnumType) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userRole, setUserRole] = useState<RoleEnumType | null>(null);
    const [userId, setUserId] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        // Check if a token exists in localStorage
        const token = localStorage.getItem('apiKey');
        if (token) {
            setIsAuthenticated(true);

            // Decode the token to get the user's role (if applicable)
            const decodedToken = decodeToken(token);
            if (decodedToken) {
                setUserRole(decodedToken.role);
                setUserId(decodedToken.id);
            } else {
                // If the token is invalid or cannot be decoded, log out the user
                localStorage.removeItem('apiKey');
                setIsAuthenticated(false);
                setUserRole(null);
                setUserId(null);
                navigate('/auth'); // Redirect to authentication page
            }
        } else {
            setIsAuthenticated(false);
            setUserRole(null);
            setUserId(null);
        }

        setIsLoading(false);
    }, []);

    const login = (token: string, role: RoleEnumType) => {
        localStorage.setItem('token', token);
        localStorage.setItem('role', role);
        setIsAuthenticated(true);
        setUserRole(role);
        navigate('/');
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        setIsAuthenticated(false);
        setUserRole(null);
        navigate('/auth');
    };

    const value = {
        isAuthenticated,
        userId,
        userRole,
        isLoading,
        login,
        logout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Helper function to decode the JWT token
const decodeToken = (token: string): JwtPayloadType | null => {
    try {
        // JWT tokens are in the format: header.payload.signature
        const payload = token.split('.')[1]; // Get the payload part
        const decodedPayload = atob(payload); // Decode base64
        const parsed = JSON.parse(decodedPayload); // Parse the JSON payload

        const result = jwtPayloadSchema.safeParse(parsed);
        if (!result.success) {
            console.error(result.error);
            return null;
        }

        return result.data;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
};

export default useAuth;


export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
