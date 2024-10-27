import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

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

const AdminStudPerformance = ({ enrollmentByGrade, performanceBySubject }) => {
    // Data for charts
    const [studentEnrollmentData, setStudentEnrollmentData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Student Enrollment by Grade',
                data: [],
                borderColor: '#3e95cd',
                backgroundColor: '#7bb6dd',
                fill: false,
            },
        ],
    });

    const [ subjectPerformanceData, setSubjectPerformanceData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Average Performance (%)',
                data: [],
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
    });

    useEffect(() => {
        if (enrollmentByGrade) {
            const grades = enrollmentByGrade.map(item => `Grade ${item.grade}`);
            const studentCounts = enrollmentByGrade.map(item => item.student_count);

            setStudentEnrollmentData({
                labels: grades,
                datasets: [
                    {
                        ...studentEnrollmentData.datasets[0],
                        data: studentCounts,
                    },
                ],
            });
        }
        if (performanceBySubject) {
            const subjects = performanceBySubject.map(item => item.subject);
            const averagePerformance = performanceBySubject.map(item => item.average_percentage);

            setSubjectPerformanceData({
            labels: subjects,
            datasets: [
                {
                ...subjectPerformanceData.datasets[0],
                data: averagePerformance,
                },
            ],
            });
        }
        }, [enrollmentByGrade, performanceBySubject]);



    return (
        <>
            <h2>School Overview</h2>
            <div className="admin-manage-container">
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
                </div>
            </div>
        </>
    );
};

export default AdminStudPerformance;
