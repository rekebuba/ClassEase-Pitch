import React from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import AdminPanel from '../components/AdminPanel';
import AdminHeader from '../components/AdminHeader';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

const AdminStudPerformance = () => {
    // Data for charts
    const studentEnrollmentData = {
        labels: ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
        datasets: [
            {
                label: 'Student Enrollment by Grade',
                data: [45, 50, 40, 60, 55, 50, 60, 70, 65, 55, 60, 75],
                borderColor: '#3e95cd',
                backgroundColor: '#7bb6dd',
                fill: false,
            },
        ],
    };

    const subjectPerformanceData = {
        labels: ['Math', 'Science', 'English', 'History', 'Geography', 'Computer Science'],
        datasets: [
            {
                label: 'Average Performance (%)',
                data: [85, 78, 90, 75, 80, 88],
                backgroundColor: [
                    '#ff6384',
                    '#36a2eb',
                    '#cc65fe',
                    '#ffce56',
                    '#fd7f6f',
                    '#6a75ff',
                ],
            },
        ],
    };

    // const budgetDistributionData = {
    //     labels: ['Salaries', 'Infrastructure', 'Resources', 'Extracurricular Activities', 'Miscellaneous'],
    //     datasets: [
    //         {
    //             data: [50, 20, 15, 10, 5],
    //             backgroundColor: ['#4caf50', '#ff9800', '#2196f3', '#9c27b0', '#ff5722'],
    //             hoverBackgroundColor: ['#66bb6a', '#ffb74d', '#42a5f5', '#ba68c8', '#ff8a65'],
    //         },
    //     ],
    // };

    // Data for teacher performance
    const classAverageData = {
        labels: ['Math', 'Science', 'English', 'History', 'Geography', 'Computer Science'],
        datasets: [
            {
                label: 'Class Average (%)',
                data: [85, 78, 90, 75, 80, 88],
                backgroundColor: '#3e95cd',
                borderColor: '#3e95cd',
                fill: false,
            },
        ],
    };

    const studentFeedbackData = {
        labels: ['Teacher A', 'Teacher B', 'Teacher C', 'Teacher D', 'Teacher E', 'Teacher F'],
        datasets: [
            {
                label: 'Feedback Score (out of 10)',
                data: [8.5, 7.8, 9.0, 7.5, 8.0, 8.8],
                backgroundColor: '#36a2eb',
            },
        ],
    };

    const teacherObservationsData = {
        labels: ['Teacher A', 'Teacher B', 'Teacher C', 'Teacher D', 'Teacher E', 'Teacher F'],
        datasets: [
            {
                label: 'Observation Score (out of 10)',
                data: [9.0, 8.5, 8.8, 8.0, 8.7, 9.1],
                backgroundColor: '#ff6384',
            },
        ],
    };

    return (
        <div className="admin-manage-container">
            <AdminPanel />
                <main className="content">
                    <AdminHeader />
                    <h2>School Overview</h2>
                    <div className="charts-container">
                        {/* Line Chart for Student Enrollment */}
                        <div className="chart-card">
                            <h3>Student Enrollment by Grade</h3>
                            <Line data={studentEnrollmentData} />
                        </div>

                        {/* Bar Chart for Subject Performance */}
                        <div className="chart-card">
                            <h3>Average Performance by Subject</h3>
                            <Bar data={subjectPerformanceData} />
                        </div>

                        {/* Pie Chart for Budget Distribution */}
                        {/* <div className="chart-card">
                    <h3>Budget Distribution</h3>
                    <Pie data={budgetDistributionData} />
                </div> */}
                        {/* Bar Chart for Classroom Observations */}
                        <div className="chart-card">
                            <h3>Classroom Observation Scores</h3>
                            <Bar data={teacherObservationsData} />
                        </div>
                        <div className="chart-card">
                            <h3>Class Averages by Subject</h3>
                            <Bar data={classAverageData} />
                        </div>
                    </div>
                </main>
        </div>
    );
};

export default AdminStudPerformance;
