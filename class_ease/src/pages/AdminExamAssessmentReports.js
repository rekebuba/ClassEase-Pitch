import React, { useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, LineElement, PointElement, ArcElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, LineElement, PointElement, ArcElement);

const ExamAssessmentReports = () => {
    const [studentPerformance, setStudentPerformance] = useState({
        subjects: ['Math', 'English', 'Science', 'History', 'Geography'],
        scores: [85, 90, 78, 88, 92],
        timePeriod: ['Semester 1', 'Semester 2', 'Semester 3'],
        progress: [
            { semester: 'Semester 1', score: 70 },
            { semester: 'Semester 2', score: 80 },
            { semester: 'Semester 3', score: 90 },
        ],
    });

    const [selectedStudent, setSelectedStudent] = useState('Student A');

    const barData = {
        labels: studentPerformance.subjects,
        datasets: [
            {
                label: 'Subject Scores',
                data: studentPerformance.scores,
                backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 99, 132, 0.6)'],
                borderWidth: 1,
            },
        ],
    };

    const lineData = {
        labels: studentPerformance.timePeriod,
        datasets: [
            {
                label: 'Progress Over Time',
                data: studentPerformance.progress.map((p) => p.score),
                fill: false,
                backgroundColor: 'rgba(75,192,192,0.6)',
                borderColor: 'rgba(75,192,192,1)',
                tension: 0.1,
            },
        ],
    };

    return (
        <div className="exam-assessment-reports">
            <div className="admin-dashboard-graph">
                <h3>This Student Performance Overview</h3>
                <div className="chart-container">
                    <div className="chart-card">
                        <h4>Subject Scores Comparison</h4>
                        <Bar data={barData} options={{ responsive: true, plugins: { legend: { display: true }, title: { display: true, text: 'Scores per Subject' } } }} />
                    </div>
                    <div className="chart-card">
                        <h4>Progress Tracking Over Time</h4>
                        <Line data={lineData} options={{ responsive: true, plugins: { legend: { display: true }, title: { display: true, text: 'Progress Over Time' } } }} />
                    </div>
                </div>
            </div>

        </div>
    );
};

export default ExamAssessmentReports;
