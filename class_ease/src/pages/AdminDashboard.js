import React, { useState, useEffect } from "react";
import "./styles/Dashboard.css";
import "./styles/AdminDashboard.css";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import AdminPanel from "../components/AdminPanel";
import ExamAssessmentReports from "./AdminExamAssessmentReports";
import AdminHeader from "../components/AdminHeader";
import AdminStudProfile from "./AdminStudProfile";

const AdminDashboard = () => {
  const [adminData, setAdminData] = useState({});
  const navigate = useNavigate();

  useEffect(
    () => {
      const retrieveData = async () => {
        try {
          const data = await api.get("/admin/dashboard");
          setAdminData(data.data);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };

      retrieveData();
    },
    [navigate]
  );

  return (
    <div className="admin-dashboard-container">
      <AdminPanel />
      <div className="content">
        <main className="dashboard-content">
          <AdminHeader />
          {/* <header className="admin-header">
            <h2>Welcome Admin</h2>
          </header> */}
          <section className="admin-stats">
            <div className="admin-stat-card">
              <h3>Total Students</h3>
              <p>350</p>
            </div>
            <div className="admin-stat-card">
              <h3>Total Teachers</h3>
              <p>45</p>
            </div>
            <div className="admin-stat-card">
              <h3>Active Classes</h3>
              <p>20</p>
            </div>
          </section>
          <AdminStudProfile />
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;
