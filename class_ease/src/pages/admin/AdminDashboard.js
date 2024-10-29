import React, { useState, useEffect } from "react";
import "../../styles/Dashboard.css";
import "../../styles/AdminDashboard.css";
import '../../styles/Table.css';
import api from "../../services/api";
import { useNavigate } from "react-router-dom";
import AdminPanel from "../../components/AdminPanel";
import AdminHeader from "../../components/AdminHeader";
import AdminStudPerformance from "./AdminStudPerformance";

/**
 * AdminDashboard component renders the main dashboard for the admin panel.
 * It fetches and displays an overview of the total number of students and teachers,
 * as well as student performance data.
 *
 * @component
 * @example
 * return (
 *   <AdminDashboard />
 * )
 *
 * @returns {JSX.Element} The rendered admin dashboard component.
 *
 * @typedef {Object} Overview
 * @property {number} total_students - The total number of students.
 * @property {number} total_teachers - The total number of teachers.
 * @property {Object} enrollment_by_grade - The enrollment data categorized by grade.
 * @property {Object} performance_by_subject - The performance data categorized by subject.
 *
 * @typedef {Object} Props
 * @property {Overview} overview - The overview data fetched from the API.
 * 
 * @function navigate
 * @description A hook from react-router-dom used for navigation.
 *
 * @function AdminPanel
 * @description A component that renders the admin panel.
 *
 * @function AdminHeader
 * @description A component that renders the admin header.
 *
 * @function AdminStudPerformance
 * @description A component that renders the student performance data.
 * @param {Object} props - The props for the AdminStudPerformance component.
 * @param {Object} props.enrollmentByGrade - The enrollment data categorized by grade.
 * @param {Object} props.performanceBySubject - The performance data categorized by subject.
 */
const AdminDashboard = () => {
  const [overview, setOverview] = useState({});

  /**
   * @function retrieveData
   * @description An asynchronous function that fetches the overview data from the API.
   */
  const retrieveData = async () => {
    try {
      const data = await api.get("/admin/overview");
      setOverview(data.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  /**
   * @function useEffect
   * @description Fetches the overview data from the API when the component mounts.
   */
  useEffect(() => {
    retrieveData();
  }, []);

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
