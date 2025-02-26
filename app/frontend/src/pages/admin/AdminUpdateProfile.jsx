import { useState, useEffect } from 'react';
import { FaUserCircle } from "react-icons/fa";
import { AdminHeader, AdminPanel } from "@/components/layout";
import { toast } from "sonner"
import { adminApi, sharedApi } from "@/api";
import '../../styles/updateProfile.css';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

/**
 * AdminUpdateProfile component allows an admin to view and update their profile information.
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
 */
const AdminUpdateProfile = () => {
    const [formData, setFormData] = useState({});
    const [previewImage, setPreviewImage] = useState('');
    const [editMode, setEditMode] = useState(false);

    /**
     * @function handleChange
     * @description Handles changes to form inputs, including file inputs for profile pictures.
     * @param {Event} e - The event object from the input change.
     */
    const handleChange = (e) => {
        const { name, value, files } = e.target;
        if (name === 'profilePicture' && files && files.length) {
            const file = files[0];
            // Validate file type and size
            if (!file.type.startsWith('image/')) {
                toast.error('Please upload a valid image file.');
                return;
            }
            if (file.size > 5 * 1024 * 1024) { // 5MB limit
                toast.error('File size should not exceed 5MB.');
                return;
            }
            const imageUrl = URL.createObjectURL(file);
            setPreviewImage(imageUrl);
            setFormData((prevData) => ({ ...prevData, [name]: file }));
        } else {
            setFormData((prevData) => ({ ...prevData, [name]: value }));
        }
        console.log(formData);
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
            const formDataToSend = new FormData();
            for (const key in formData) {
                formDataToSend.append(key, formData[key]);
            }

            console.log(formDataToSend);
            const response = await sharedApi.updateProfile(formDataToSend);
            if (response.status === 200) {
                toast.success(response.data.message, {
                    description: new Date().toLocaleString(),
                    style: { color: 'green' },
                });

            }
        } catch (error) {
            const errorMessage = error.response?.data?.error || "An unexpected error occurred.";
            toast.error(errorMessage, {
                description: "Please try again later, if the problem persists, contact the administrator.",
                style: { color: 'red' },
            });
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
     * @hook useEffect
     * @description Loads the admin data when the component mounts.
     * @returns {void}
     */
    useEffect(() => {
        let isMounted = true;
        const fetchData = async () => {
            try {
                const response = await adminApi.getDashboardData();
                if (isMounted) {
                    const data = response.data;
                    setFormData(data);
                    if (data.image_url) {
                        setPreviewImage(data.image_url);
                    }
                }
            } catch (error) {
                if (isMounted && error.response?.data) {
                    console.log(error.response.data.message);
                }
            }
        };
        fetchData();
        return () => {
            isMounted = false;
        };
    }, []);

    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <AdminHeader />
            <div className="flex flex-1 scroll-m-0">
                <AdminPanel />
                <div className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <div className="m-0 p-5">
                        <div className="profile-details">
                            <div className="flex self-start flex-col gap-5">
                                <Avatar className="w-40 h-40">
                                    <AvatarImage src={previewImage} />
                                    <AvatarFallback><FaUserCircle className="w-40 h-40 text-gray-500" /></AvatarFallback>
                                </Avatar>
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
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminUpdateProfile;
