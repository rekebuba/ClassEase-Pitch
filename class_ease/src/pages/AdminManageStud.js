import React, { useState } from "react";
import "./styles/AdminManageStudents.css";
import AdminPanel from "../components/AdminPanel";
// import { useNavigate } from "react-router-dom";
import AdminHeader from "../components/AdminHeader";
import AdminStudProfileView from "./AdminStudProfile";
import AdminStudentsList from "./AdminStudList";


const AdminManageStudents = () => {

  const [isOpen, setIsOpen] = useState(false);
  const [studentSummary, setStudentSummary] = useState({});

  const toggleDropdown = () => {
      setIsOpen(!isOpen);
  };

  const toggleProfile = () => {
    setIsOpen(false);
  }

  const summary = (data) => {
    setStudentSummary(data);
  }

  return (
    <div className="admin-manage-container">
      <AdminPanel />
      <main className="content">
        <AdminHeader />
        <AdminStudentsList toggleDropdown={toggleDropdown} studentSummary={summary} />
        <AdminStudProfileView isOpen={isOpen} toggleProfile={toggleProfile} studentData={studentSummary} />
      </main>
    </div>
  );
};

export default AdminManageStudents;