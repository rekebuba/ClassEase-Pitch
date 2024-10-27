import React, { useState } from 'react';
import Api from '../services/api';
import Alert from './Alert';
import convertKeysToSnakeCase from './library/lodash';

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


    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

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
