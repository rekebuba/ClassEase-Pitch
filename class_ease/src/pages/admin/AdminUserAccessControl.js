import React, { useState, useEffect } from 'react';
import AdminPanel from '../../components/AdminPanel';
import AdminHeader from '../../components/AdminHeader';


// Mock Data for Users and Roles
const initialUsers = [
    { id: 1, name: 'John Doe', role: 'Teacher', lastActivity: 'Updated student grades', activityDate: '2024-10-09' },
    { id: 2, name: 'Jane Smith', role: 'Admin', lastActivity: 'Added new teacher', activityDate: '2024-10-08' },
    { id: 3, name: 'Mark Johnson', role: 'Staff', lastActivity: 'Updated attendance', activityDate: '2024-10-07' },
];

const roles = ['Admin', 'Teacher', 'Staff'];

const AdminUserAccessControl = () => {
    const [users, setUsers] = useState(initialUsers);
    const [newUser, setNewUser] = useState({ name: '', role: '' });
    const [activityLog, setActivityLog] = useState([]);

    useEffect(() => {
        // Initialize the activity log with mock data
        setActivityLog(users.map(user => ({
            name: user.name,
            lastActivity: user.lastActivity,
            date: user.activityDate,
        })));
    }, [users]);

    const handleUserInputChange = (e) => {
        setNewUser({ ...newUser, [e.target.name]: e.target.value });
    };

    const addUser = () => {
        const newUserWithId = { id: users.length + 1, ...newUser, lastActivity: 'User Created', activityDate: new Date().toISOString().split('T')[0] };
        setUsers([...users, newUserWithId]);
        setActivityLog([...activityLog, { name: newUser.name, lastActivity: 'User Created', date: new Date().toISOString().split('T')[0] }]);
        setNewUser({ name: '', role: '' });
    };

    const updateUserRole = (id, newRole) => {
        const updatedUsers = users.map(user => (user.id === id ? { ...user, role: newRole, lastActivity: 'Role Updated', activityDate: new Date().toISOString().split('T')[0] } : user));
        setUsers(updatedUsers);
        const updatedUser = updatedUsers.find(user => user.id === id);
        setActivityLog([...activityLog, { name: updatedUser.name, lastActivity: 'Role Updated', date: new Date().toISOString().split('T')[0] }]);
    };

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            {/* Add New User Section */}
            <main className="content">
                <AdminHeader />
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
            </main>
        </div>
    );
};

export default AdminUserAccessControl;
