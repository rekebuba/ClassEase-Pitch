import React, { useState, useEffect } from 'react';
import '../../styles/updateProfile.css';
import AdminHeader from '../../components/AdminHeader';
import AdminPanel from '../../components/AdminPanel';
import api from '../../services/api';
import Alert from '../../services/Alert';

/**
 * AdminUpdateProfile component allows an admin to view and update their profile information.
 * 
 * @component
 * @returns {JSX.Element} The rendered component.
 * 
 * @example
 * return (
 *   <AdminUpdateProfile />
 * )
 * 
 * @description
 * This component fetches the admin's profile data from the server and displays it. 
 * It allows the admin to edit their profile information, including their profile picture, 
 * name, email, phone, address, and password. The component also handles file input for 
 * profile picture updates and displays alerts for success or error messages.
 * 
 * @function
 * @name AdminUpdateProfile
 * 
 * @property {Object} formData - The state object holding the form data.
 * @property {Function} setFormData - The function to update the formData state.
 * @property {string} previewImage - The state holding the URL of the preview image.
 * @property {Function} setPreviewImage - The function to update the previewImage state.
 * @property {boolean} editMode - The state indicating whether the form is in edit mode.
 * @property {Function} setEditMode - The function to update the editMode state.
 * @property {Object} alert - The state object holding alert information.
 * @property {Function} setAlert - The function to update the alert state.
 */
const AdminUpdateProfile = () => {
    const [formData, setFormData] = useState({});
    const [previewImage, setPreviewImage] = useState('');
    const [editMode, setEditMode] = useState(false);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });

    /**
     * @function handleChange
     * @description Handles changes to form inputs, including file inputs for profile pictures.
     * @param {Event} e - The event object from the input change.
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
     * @function loadAdminData
     * @description Fetches the admin's profile data from the server and updates the formData state.
     * @async
     * @returns {Promise<void>}
     */
    const loadAdminData = async () => {
        try {
            const response = await api.get(`/admin/dashboard`);
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
     * @function saveAdminData
     * @description Sends the updated profile data to the server to save the changes.
     * @async
     * @returns {Promise<void>}
     * @throws {Alert} An alert with a success or warning message.
     * @throws {Alert} An alert with a warning message if an unexpected error occurs.
     */
    const saveAdminData = async () => {
        try {
            const response = await api.put(`/admin/update-profile`, formData);
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
     * @description Handles the save button click, exits edit mode, and saves the profile data.
     * @returns {void}
     */
    const handleSave = () => {
        setEditMode(false);
        saveAdminData();
    };

    /**
     * @function showAlert
     * @description Displays an alert with the specified type and message.
     * @param {string} type - The type of the alert (e.g., "success", "warning").
     * @param {string} message - The message to display in the alert.
     * @returns {void}
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert
     * @description Closes the alert.
     * @returns {void}
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @hook useEffect
     * @description Loads the admin data when the component mounts.
     * @returns {void}
     */
    useEffect(() => {
        loadAdminData();
    }, []);

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <div className="user-profile">
                    <AdminHeader />
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
                                        name="name"
                                        value={formData.name || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.name}</p>
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

export default AdminUpdateProfile;
