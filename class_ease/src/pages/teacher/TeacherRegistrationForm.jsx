import React, { useState } from 'react';
import Api from '../../services/api';
import Alert from '../../services/Alert';
import convertKeysToSnakeCase from '../library/lodash';

/**
 * TeacherRegistrationForm Component
 * 
 * This component renders a form for registering a new teacher. It includes fields for 
 * first name, last name, age, gender, email, phone number, address, subjects taught, 
 * qualifications, and years of experience. The form data is managed using React's 
 * useState hook, and form submission is handled asynchronously with error handling.
 * 
 * @component
 * @example
 * return (
 *   <TeacherRegistrationForm />
 * )
 * 
 * @returns {JSX.Element} The rendered component.
 * 
 * @function
 * @name TeacherRegistrationForm
 * 
 * @description
 * - `showAlert(type, message)`: Displays an alert with the specified type and message.
 * - `closeAlert()`: Closes the currently displayed alert.
 * - `handleChange(e)`: Updates the form data state when an input field value changes.
 * - `handleSubmit(e)`: Handles form submission, converts form data to snake_case, 
 *   sends a POST request to the server, and displays success or error alerts based 
 *   on the response.
 * 
 * @state {Object} alert - The state object for managing alert visibility and content.
 * @state {string} alert.type - The type of the alert (e.g., "success", "warning").
 * @state {string} alert.message - The message to be displayed in the alert.
 * @state {boolean} alert.show - A flag indicating whether the alert is visible.
 * 
 * @state {Object} formData - The state object for managing form input values.
 * @state {string} formData.firstName - The first name of the teacher.
 * @state {string} formData.lastName - The last name of the teacher.
 * @state {string} formData.age - The age of the teacher.
 * @state {string} formData.gender - The gender of the teacher.
 * @state {string} formData.email - The email address of the teacher.
 * @state {string} formData.phone - The phone number of the teacher.
 * @state {string} formData.address - The address of the teacher.
 * @state {string} formData.experience - The years of experience of the teacher.
 * @state {string} formData.qualification - The qualifications of the teacher.
 * @state {string} formData.subjectTaught - The subjects taught by the teacher.
 * 
 * @dependencies
 * - `useState`: React hook for managing state.
 * - `Api`: Custom API utility for making HTTP requests.
 * - `convertKeysToSnakeCase`: Utility function for converting object keys to snake_case.
 * - `Alert`: Custom Alert component for displaying messages.
 */
const TeacherRegistrationForm = () => {
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        age: '',
        gender: '',
        email: '',
        phone: '',
        address: '',
        experience: '',
        qualification: '',
        subjectTaught: '',
    });

    /**
     * @function showAlert
     * @description Sets the alert message.
     * @param {string} type - Type of the alert.
     * @param {string} message - Message to display in the alert.
     * @returns {void}
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert
     * @description Closes the alert message.
     * @returns {void}
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @function handleChange
     * @description Updates the form data state when an input field value changes.
     * @param {Object} e - The event object.
     * @returns {void}
     */
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    /**
     * @function handleSubmit
     * @description Handles form submission, converts form data to snake_case,
     * sends a POST request to the server, and displays success or error alerts based
     * on the response.
     * @param {Object} e - The event object.
     * @returns {void}
     * @async
     * @throws {error} An error occurred while processing the request.
     * @throws {error.response.data.error} An error message returned by the server.
     * @throws {error.response.data} An unexpected error occurred.
     * @returns {void}
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = convertKeysToSnakeCase(formData);
        try {
            await Api.post('/admin/teachers/registration', data);
            showAlert("success", "Teacher registered successfully!");
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
                console.error(error.response.data['error']);
            } else {
                showAlert("warning", "An unexpected error occurred.");
            }
        }
    };

    return (
        <div className="teacher-registration-form">
            <h2>Teacher Registration Form</h2>
            <form onSubmit={handleSubmit}>
                <div className="teacher-registration-form-group">
                    <label htmlFor="firstName">First Name</label>
                    <input
                        type="text"
                        id="firstName"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="lastName">Last Name</label>
                    <input
                        type="text"
                        id="lastName"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="age">Age</label>
                    <input
                        type="number"
                        id="age"
                        name="age"
                        value={formData.age}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="gender">Gender</label>
                    <select
                        id="gender"
                        name="gender"
                        value={formData.gender}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="phone">Phone Number</label>
                    <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="address">Address</label>
                    <input
                        type="text"
                        id="address"
                        name="address"
                        value={formData.address}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="subjectTaught">Subjects Taught</label>
                    <input
                        type="text"
                        id="subjectTaught"
                        name="subjectTaught"
                        value={formData.subjectTaught}
                        onChange={handleChange}
                        placeholder="e.g., Math, Physics"
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="qualification">Qualifications</label>
                    <input
                        type="text"
                        id="qualification"
                        name="qualification"
                        value={formData.qualification}
                        onChange={handleChange}
                        placeholder="e.g., B.Sc. in Mathematics"
                        required
                    />
                </div>
                <div className="teacher-registration-form-group">
                    <label htmlFor="experience">Years of Experience</label>
                    <input
                        type="number"
                        id="experience"
                        name="experience"
                        value={formData.experience}
                        onChange={handleChange}
                        required
                    />
                </div>
                <Alert
                    type={alert.type}
                    message={alert.message}
                    show={alert.show}
                    onClose={closeAlert}
                />
                <button type="submit" className="teacher-registration-submit-btn">Register</button>
            </form>
        </div>
    );
};

export default TeacherRegistrationForm;
