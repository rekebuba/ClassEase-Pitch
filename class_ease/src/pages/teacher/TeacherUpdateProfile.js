import React, { useState, useEffect } from 'react';
import '../../styles/updateProfile.css';
import TeacherHeader from '../../components/TeachHeader';
import TeacherPanel from '../../components/TeachPanel';
import api from '../../services/api';
import Alert from '../../services/Alert';

/**
 * TeacherUpdateProfile component allows teachers to update their profile information.
 * It includes functionalities for loading existing teacher data, handling form changes,
 * previewing profile pictures, and saving updated data.
 *
 * @component
 * @example
 * return (
 *   <TeacherUpdateProfile />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @function
 * @name TeacherUpdateProfile
 *
 * @description
 * This component manages the state for form data, preview image, edit mode, and alert messages.
 * It provides functions to handle form changes, load teacher data from the server, save updated
 * data to the server, and display alert messages.
 *
 * @property {Object} formData - The state object holding the form data.
 * @property {string} previewImage - The state string holding the URL of the preview image.
 * @property {boolean} editMode - The state boolean indicating whether the form is in edit mode.
 * @property {Object} alert - The state object holding alert message details.
 */
const TeacherUpdateProfile = () => {
    const [formData, setFormData] = useState({});
    const [previewImage, setPreviewImage] = useState('');
    const [editMode, setEditMode] = useState(false);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });

    /**
     * @function handleChange
     * @description Handles changes in the form inputs and updates the formData state.
     * @param {Object} e - The event object.
     * @returns {void}
     */
    const handleChange = (e) => {
        const { name, value, files } = e.target;
        if (name === 'profilePicture' && files.length) {
            const imageUrl = URL.createObjectURL(files[0]);
            setPreviewImage(imageUrl);
            setFormData((prevData) => ({ ...prevData, [name]: files[0] }));
        } else {
            setFormData((prevData) => ({ ...prevData, [name]: value }));
        }
    };

    /**
     * @function loadTeacherData
     * @description Loads the teacher's data from the server and updates the formData and previewImage states.
     * @returns {void}
     * @async
     * @throws {error} Any error while fetching the data.
     * @throws {error.response.data.message} The error message received from the server.
     */
    const loadTeacherData = async () => {
        try {
            const response = await api.get(`/teacher/dashboard`);
            const data = response.data;
            console.log(data);
            setFormData(data);
            if (data.profilePicture) {
                setPreviewImage(data.profilePicture);
            }
        } catch (error) {
            if (error.response && error.response.data) {
                console.log(error.response.data.message);
            }
        }
    };

    /**
     * @function saveTeacherData
     * @description Sends the updated formData to the server to save the changes.
     * @returns {void}
     * @async
     * @throws {error} Any error while saving the data.
     * @throws {error.response.data.error} The error message received from the server.
     * @throws {error.response.data.message} The success message received from the server.
     * @throws {error.response.data} The unexpected error message received from the server.
     */
    const saveTeacherData = async () => {
        try {
            const response = await api.put(`/teacher/update-profile`, formData);
            console.log(response.data);
            showAlert("success", response.data.message);
        } catch (error) {
            if (error.response && error.response.data) {
                showAlert("warning", error.response.data['error']);
            }
            else {
                showAlert("warning", "An unexpected error occurred.");
            }
        }
    };

    /**
     * @function handleSave
     * @description Disables edit mode and calls saveTeacherData to save the changes.
     * @returns {void}
     */
    const handleSave = () => {
        setEditMode(false);
        saveTeacherData();
    };

    /**
     * @function showAlert
     * @description Displays an alert message with the specified type and message.
     * @param {string} type - The type of the alert message.
     * @param {string} message - The message to display in the alert.
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
     * @hook useEffect
     * @description Loads the teacher's data when the component mounts.
     * @returns {void}
     */
    useEffect(() => {
        loadTeacherData();
    }, []);

    return (
        <div className="admin-manage-container">
            <TeacherPanel />
            <main className="content">
                <div className="user-profile">
                    <TeacherHeader />
                    <h2>User Profile</h2>

                    <div className="profile-details">
                        <div className="profile-picture">
                            <img src={previewImage} alt="Profile" />
                            {editMode && (
                                <input type="file" name="profilePicture" onChange={handleChange} />
                            )}
                        </div>
                        <div className='profile-data'>
                            <div className="profile-form-group">
                                <label>Name</label>
                                {editMode ? (
                                    <input
                                        type="text"
                                        name="first_name"
                                        value={formData.first_name || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.first_name}</p>
                                )}
                            </div>

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Email</label>
                                {editMode ? (
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.email}</p>
                                )}
                            </div>

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Phone</label>
                                {editMode ? (
                                    <input
                                        type="tel"
                                        name="phone"
                                        value={formData.phone || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.phone}</p>
                                )}
                            </div>

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Address</label>
                                {editMode ? (
                                    <input
                                        type="text"
                                        name="address"
                                        value={formData.address || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.address}</p>
                                )}
                            </div>
                            {editMode &&
                                <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                    <label>Current Password</label>
                                    <input
                                        type="password"
                                        name="current_password"
                                        placeholder="Enter current password"
                                        onChange={handleChange}
                                    />
                                </div>
                            }

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Password</label>
                                {editMode ? (
                                    <input
                                        type="password"
                                        name="new_password"
                                        placeholder="Enter new password"
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>********</p>
                                )}
                            </div>
                        </div>
                    </div>

                    <div className="button-group">
                        {editMode ? (
                            <>
                                <button className="save-button" onClick={handleSave}>
                                    Save Changes
                                </button>
                                <button className="cancel-button" onClick={() => setEditMode(false)}>
                                    Cancel
                                </button>
                            </>
                        ) : (
                            <button className="edit-button" onClick={() => setEditMode(true)}>
                                Edit Profile
                            </button>
                        )}
                    </div>
                    <Alert
                        type={alert.type}
                        message={alert.message}
                        show={alert.show}
                        onClose={closeAlert}
                    />
                </div>
            </main>
        </div>
    );
};

export default TeacherUpdateProfile;