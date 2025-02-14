import { useState, useEffect } from 'react';
import { StudentPanel } from "@/components/layout";
import { api } from "@/api";
import { toast } from "sonner"
import '../../styles/updateProfile.css';

/**
 * Component for updating student profile.
 *
 * @component
 * @example
 * return (
 *   <StudentUpdateProfile />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @description
 * This component allows students to update their profile information. It includes fields for profile picture, name, date of birth, father's phone, mother's phone, and password. The component fetches the current student data on mount and displays it. Users can toggle between view and edit modes. In edit mode, users can update their information and save changes.
 *
 * @function
 * @name StudentUpdateProfile
 *
 * @property {Object} formData - The state object holding form data.
 * @property {string} previewImage - The state string holding the URL of the preview image.
 * @property {boolean} editMode - The state boolean indicating if the form is in edit mode.
 * @property {Object} alert - The state object holding alert information.
 * @property {string} alert.type - The type of alert (e.g., "success", "warning").
 * @property {string} alert.message - The alert message.
 * @property {boolean} alert.show - Boolean indicating if the alert is visible.
 */
const StudentUpdateProfile = () => {
    const [formData, setFormData] = useState({});
    const [previewImage, setPreviewImage] = useState('');
    const [editMode, setEditMode] = useState(false);

    /**
     * @function handleChange
     * @description Handles changes to form inputs and updates the state.
     * @param {Event} e - The event object.
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
     * @function loadStudentData
     * @description Fetches student data from the API and updates the state.
     * @returns {void}
     * @async
     * @throws {error} Any error while fetching data.
     */
    const loadStudentData = async () => {
        try {
            const response = await api.get(`/student/dashboard`);
            const data = response.data;
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
     * @function saveStudentData
     * @description Sends updated student data to the API to save changes.
     * @returns {void}
     * @async
     * @throws {error} Any error while saving data.
     * @throws {error} An error if the form submission fails.
     * @throws {error} An unexpected error occurred.
     */
    const saveStudentData = async () => {
        try {
            const response = await api.put(`/student/update-profile`, formData);
            console.log(response.data);
            toast.success(response.data['message'], {
                description: currentTime,
                style: { color: 'green' }
            });
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            } else {
                toast.error("An unexpected error occurred.", {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
    };

    /**
     * @function handleSave
     * @description Handles the save button click, toggles edit mode off, and saves student data.
     * @returns {void}
     */
    const handleSave = () => {
        setEditMode(false);
        saveStudentData();
    };

    /**
     * @hook useEffect
     * @description Loads student data on component mount.
     * @returns {void}
     */
    useEffect(() => {
        loadStudentData();
    }, []);

    return (
        <div className="admin-manage-container">
            <StudentPanel />
            <main className="content">
                <header className="dashboard-header">
                    <div className="dashboard-logo">ClassEase School</div>
                </header>
                <div className="user-profile">
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
                                <p>{formData.name} {formData.father_name} {formData.grand_father_name}</p>
                            </div>
                            <div className="profile-form-group">
                                <label htmlFor="dateOfBirth">Date of Birth</label>
                                {editMode ? (
                                    <input
                                        type="date"
                                        id="dateOfBirth"
                                        name="date_of_birth"
                                        value={formData.date_of_birth || ''}
                                        onChange={handleChange}
                                        required
                                    />
                                ) : (
                                    <p>{formData.date_of_birth}</p>
                                )}
                            </div>

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Father Phone</label>
                                {editMode ? (
                                    <input
                                        type="tel"
                                        name="father_phone"
                                        value={formData.father_phone || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.father_phone}</p>
                                )}
                            </div>

                            <div className="profile-form-group" style={{ marginBottom: '15px' }}>
                                <label>Mother Phone</label>
                                {editMode ? (
                                    <input
                                        type="tel"
                                        name="mother_phone"
                                        value={formData.mother_phone || ''}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    <p>{formData.mother_phone}</p>
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
                </div>
            </main>
        </div>
    );
};

export default StudentUpdateProfile;
