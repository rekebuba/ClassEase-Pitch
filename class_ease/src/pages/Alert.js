import React, { useEffect } from "react";
import "./styles/Alert.css";

const Alert = ({ type, message, show, onClose }) => {
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
