import { useState, useEffect } from 'react';
import { AdminHeader, AdminPanel } from "@/components/layout";



// Mock Data for Users and Roles
const initialUsers = [
    { id: 1, name: 'John Doe', role: 'Teacher', lastActivity: 'Updated student grades', activityDate: '2024-10-09' },
    { id: 2, name: 'Jane Smith', role: 'Admin', lastActivity: 'Added new teacher', activityDate: '2024-10-08' },
    { id: 3, name: 'Mark Johnson', role: 'Staff', lastActivity: 'Updated attendance', activityDate: '2024-10-07' },
];

const roles = ['Admin', 'Teacher', 'Staff'];

/**
 * AdminUserAccessControl component manages user access control for the admin panel.
 * It allows adding new users, updating user roles, and viewing user activity logs.
 *
 * @component
 * @example
 * return (
 *   <AdminUserAccessControl />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @function
 * @name AdminUserAccessControl
 *
 * @description
 * - Initializes the user list and activity log with mock data.
 * - Provides functionality to add new users.
 * - Allows updating user roles.
 * - Displays a list of users with their details and actions.
 * - Shows a log of user activities.
 *
 * @hook
 * @name useState
 * @description Manages the state for users, new user input, and activity log.
 *
 * @hook
 * @name useEffect
 * @description Initializes the activity log whenever the user list changes.
 *
 * @param {Object} newUser - The new user being added.
 * @param {string} newUser.name - The name of the new user.
 * @param {string} newUser.role - The role of the new user.
 *
 * @param {Array} users - The list of users.
 * @param {number} users.id - The unique ID of the user.
 * @param {string} users.name - The name of the user.
 * @param {string} users.role - The role of the user.
 * @param {string} users.lastActivity - The last activity performed by the user.
 * @param {string} users.activityDate - The date of the last activity.
 *
 * @param {Array} activityLog - The log of user activities.
 * @param {string} activityLog.name - The name of the user who performed the activity.
 * @param {string} activityLog.lastActivity - The last activity performed by the user.
 * @param {string} activityLog.date - The date of the activity.
 *
 * @function handleUserInputChange
 * @description Handles changes to the new user input fields.
 * @param {Object} e - The event object.
 *
 * @function addUser
 * @description Adds a new user to the user list and updates the activity log.
 *
 * @function updateUserRole
 * @description Updates the role of an existing user and logs the activity.
 * @param {number} id - The ID of the user to update.
 * @param {string} newRole - The new role to assign to the user.
 */
const AdminUserAccessControl = () => {
    const [users, setUsers] = useState(initialUsers);
    const [newUser, setNewUser] = useState({ name: '', role: '' });
    const [activityLog, setActivityLog] = useState([]);

    /**
     * @hook useEffect
     * @description Initializes the activity log whenever the user list changes.
     * @param {Array} users - The list of users.
     * @param {Array} activityLog - The log of user activities.
     */
    useEffect(() => {
        // Initialize the activity log with mock data
        setActivityLog(users.map(user => ({
            name: user.name,
            lastActivity: user.lastActivity,
            date: user.activityDate,
        })));
    }, [users]);

    /**
     * @function handleUserInputChange
     * @description Handles changes to the new user input fields.
     * @param {Object} e - The event object.
     * @param {string} e.target.name - The name of the input field.
     * @param {string} e.target.value - The value of the input field.
     */
    const handleUserInputChange = (e) => {
        setNewUser({ ...newUser, [e.target.name]: e.target.value });
    };

    /**
     * @function addUser
     * @description Adds a new user to the user list and updates the activity log.
     * @param {Object} newUser - The new user being added.
     * @param {string} newUser.name - The name of the new user.
     * @param {string} newUser.role - The role of the new user.
     * @param {Array} users - The list of users.
     * @param {Array} activityLog - The log of user activities.
     * @param {Array} setUsers - The function to update the user list.
     * @param {Array} setActivityLog - The function to update the activity log.
     * @param {Object} newDate - The current date and time.
     * @param {string} newDate.toISOString() - The current date and time in ISO format.
     * @param {string} newDate.toISOString().split('T')[0] - The current date.
     * @param {Object} newUserWithId - The new user with a unique ID.
     * @param {number} users.length - The number of users in the list.
     */
    const addUser = () => {
        const newUserWithId = { id: users.length + 1, ...newUser, lastActivity: 'User Created', activityDate: new Date().toISOString().split('T')[0] };
        setUsers([...users, newUserWithId]);
        setActivityLog([...activityLog, { name: newUser.name, lastActivity: 'User Created', date: new Date().toISOString().split('T')[0] }]);
        setNewUser({ name: '', role: '' });
    };

    /**
     * @function updateUserRole
     * @description Updates the role of an existing user and logs the activity.
     * @param {number} id - The ID of the user to update.
     * @param {string} newRole - The new role to assign to the user.
     * @param {Array} users - The list of users.
     */
    const updateUserRole = (id, newRole) => {
        const updatedUsers = users.map(user => (user.id === id ? { ...user, role: newRole, lastActivity: 'Role Updated', activityDate: new Date().toISOString().split('T')[0] } : user));
        setUsers(updatedUsers);
        const updatedUser = updatedUsers.find(user => user.id === id);
        setActivityLog([...activityLog, { name: updatedUser.name, lastActivity: 'Role Updated', date: new Date().toISOString().split('T')[0] }]);
    };

    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <AdminHeader />
            <div className="flex flex-1 scroll-m-0">
                <AdminPanel />
                <div className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <h2 className="access-control-h2">User Access Control</h2>

                    <div className="add-user">
                        <h3>Add New User</h3>
                        <input
                            type="text"
                            placeholder="User Name"
                            name="name"
                            value={newUser.name}
                            onChange={handleUserInputChange}
                        />
                        <select name="role" value={newUser.role} onChange={handleUserInputChange}>
                            <option value="">Select Role</option>
                            {roles.map(role => (
                                <option key={role} value={role}>
                                    {role}
                                </option>
                            ))}
                        </select>
                        <button onClick={addUser} disabled={!newUser.name || !newUser.role}>
                            Add User
                        </button>
                    </div>

                    {/* User List Section */}
                    <div className="user-list">
                        <h3>Manage Users</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Role</th>
                                    <th>Last Activity</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map(user => (
                                    <tr key={user.id}>
                                        <td>{user.id}</td>
                                        <td>{user.name}</td>
                                        <td>
                                            <select
                                                value={user.role}
                                                onChange={e => updateUserRole(user.id, e.target.value)}
                                            >
                                                {roles.map(role => (
                                                    <option key={role} value={role}>
                                                        {role}
                                                    </option>
                                                ))}
                                            </select>
                                        </td>
                                        <td>{user.lastActivity} on {user.activityDate}</td>
                                        <td>
                                            <button className="delete-btn" onClick={() => setUsers(users.filter(u => u.id !== user.id))}>
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Activity Log Section */}
                    <div className="activity-log">
                        <h3>User Activity Log</h3>
                        <ul>
                            {activityLog.map((log, index) => (
                                <li key={index}>
                                    <strong>{log.name}</strong> - {log.lastActivity} on {log.date}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminUserAccessControl;
