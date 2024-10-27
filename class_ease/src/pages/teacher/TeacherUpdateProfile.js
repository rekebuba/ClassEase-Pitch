import React, { useState, useEffect } from 'react';
import '../../styles/updateProfile.css';
import TeacherHeader from '../../components/TeachHeader';
import TeacherPanel from '../../components/TeachPanel';
import api from '../../services/api';
import Alert from '../../services/Alert';

const TeacherUpdateProfile = () => {
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

    const handleSave = () => {
        setEditMode(false);
        saveTeacherData();
    };

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

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
