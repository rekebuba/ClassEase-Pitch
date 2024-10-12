import React from 'react';
import AdminPanel from '../components/AdminPanel';
import AdminHeader from '../components/AdminHeader';
import StudentRegistrationForm from './StudRegistrationForm';

const AdminEnrollStud = () => {

    return (
        <div className="admin-dashboard-container">
            <AdminPanel />
            <div className="content">
                <main className="dashboard-content">
                    <AdminHeader />
                    <StudentRegistrationForm />
                </main>
            </div>
        </div>
    );
}


export default AdminEnrollStud;
