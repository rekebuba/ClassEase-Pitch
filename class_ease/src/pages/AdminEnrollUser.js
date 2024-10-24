import React from 'react';
import AdminPanel from '../components/AdminPanel';
import AdminHeader from '../components/AdminHeader';
import StudentRegistrationForm from './StudRegistrationForm';
import TeacherRegistrationForm from './TeacherRegistrationForm';

const AdminEnrollStud = ({ role }) => {

    return (
        <div className="admin-dashboard-container">
            <AdminPanel />
            <div className="content">
                <main className="dashboard-content">
                    <AdminHeader />
                    {role === 'teacher' ? <TeacherRegistrationForm /> : <StudentRegistrationForm />
                    }
                </main>
            </div>
        </div>
    );
}


export default AdminEnrollStud;