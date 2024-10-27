import React, { useState, useEffect } from "react";
import "../../styles/Dashboard.css";
import "../../styles/AdminDashboard.css";
import '../../styles/Table.css';
import api from "../../services/api";
import { useNavigate } from "react-router-dom";
import AdminPanel from "../../components/AdminPanel";
import AdminHeader from "../../components/AdminHeader";
import AdminStudPerformance from "./AdminStudPerformance";

const AdminDashboard = () => {
  const [overview, setOverview] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const retrieveData = async () => {
      try {
        const data = await api.get("/admin/overview");
        setOverview(data.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    retrieveData();
  }, [navigate]);

  return (
    <div className="admin-dashboard-container">
      <AdminPanel />
      <div className="content">
        <main className="dashboard-content">
          <AdminHeader />
          <section className="admin-stats">
            <div className="admin-stat-card">
              <h3>Total Students</h3>
              <p>{overview.total_students}</p>
            </div>
            <div className="admin-stat-card">
              <h3>Total Teachers</h3>
              <p>{overview.total_teachers}</p>
            </div>
          </section>
          <AdminStudPerformance
            enrollmentByGrade={overview.enrollment_by_grade}
            performanceBySubject={overview.performance_by_subject}
          />
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;
