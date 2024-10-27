import React, { useState, useEffect } from 'react';
import '../../styles/updateProfile.css';
import StudentPanel from '../../components/StdPanel';
import api from '../../services/api';
import Alert from '../../services/Alert';

const StudentUpdateProfile = () => {
    const [formData, setFormData] = useState({});
    const [previewImage, setPreviewImage] = useState('');
    const [editMode, setEditMode] = useState(false);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });


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

    const loadStudentData = async () => {
        try {
            const response = await api.get(`/student/dashboard`);
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

    const saveStudentData = async () => {
        try {
            const response = await api.put(`/student/update-profile`, formData);
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

    const handleSave = () => {
        setEditMode(false);
        saveStudentData();
    };

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

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

export default StudentUpdateProfile;
