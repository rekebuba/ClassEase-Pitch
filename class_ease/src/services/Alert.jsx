import React, { useEffect } from "react";
import "../styles/Alert.css";

/**
 * Alert component that displays a message with a specific type and automatically closes after a set duration.
 *
 * @component
 * @param {Object} props - The properties object.
 * @param {string} props.type - The type of alert (e.g., 'success', 'error', 'warning').
 * @param {string} props.message - The message to display in the alert.
 * @param {boolean} props.show - A boolean indicating whether the alert should be shown.
 * @param {Function} props.onClose - A callback function to be called when the alert automatically closes.
 *
 * @example
 * <Alert 
 *   type="success" 
 *   message="Operation completed successfully!" 
 *   show={true} 
 *   onClose={() => console.log('Alert closed')} 
 * />
 *
 * @returns {JSX.Element|null} The Alert component or null if not shown.
 */
const Alert = ({ type, message, show, onClose }) => {
    /**
     * Automatically close the alert after 5 seconds.
     */
    useEffect(() => {
        let timer;

        if (show) {
            // Clear any existing timer to ensure it resets on each show
            timer = setTimeout(() => {
                onClose(); // Automatically close after 5 seconds
            }, 5000);
        }

        // Cleanup the timer when the component unmounts or when show changes
        return () => clearTimeout(timer);
    }, [show, onClose]); // Reset the timer whenever "show" changes

    if (!show) return null;

    return (
        <div className={`alert alert-${type} alert-show`}>
            <p>{message}</p>
            <div className="progress-bar"></div>
        </div>
    );
};

export default Alert;
