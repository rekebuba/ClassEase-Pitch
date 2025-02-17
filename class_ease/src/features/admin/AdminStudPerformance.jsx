import { useState, useEffect } from 'react';
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

/**
 * AdminStudPerformance Component
 * 
 * This component displays the student enrollment by grade and average performance by subject
 * using line and bar charts respectively. It takes in two props: `enrollmentByGrade` and 
 * `performanceBySubject`, which are arrays of objects containing the necessary data for the charts.
 * 
 * Props:
 * @param {Object[]} enrollmentByGrade - Array of objects representing student enrollment by grade.
 * @param {number} enrollmentByGrade[].grade - The grade level.
 * @param {number} enrollmentByGrade[].student_count - The number of students enrolled in the grade.
 * 
 * @param {Object[]} performanceBySubject - Array of objects representing performance by subject.
 * @param {string} performanceBySubject[].subject - The name of the subject.
 * @param {number} performanceBySubject[].average_percentage - The average performance percentage in the subject.
 * 
 * @returns {JSX.Element} The rendered component displaying the charts.
 * 
 * Example usage:
 * <AdminStudPerformance 
 *    enrollmentByGrade={[{ grade: 1, student_count: 30 }, { grade: 2, student_count: 25 }]} 
 *    performanceBySubject={[{ subject: 'Math', average_percentage: 75 }, { subject: 'Science', average_percentage: 80 }]} 
 * />
 */
const AdminStudentPerformance = ({ enrollmentByGrade, performanceBySubject }) => {
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

    /**
     * @description Updates the data for the student enrollment and subject performance charts
    */
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
            <div className="flex h-full">
                <div className="flex flex-wrap justify-between w-full h-fit">
                    {/* Line Chart for Student Enrollment */}
                    <div className="bg-white p-5 m-3 max-w-lg h-1/2 w-full">
                        <h3>Student Enrollment by Grade</h3>
                        <Line data={studentEnrollmentData} />
                    </div>
                    {/* Bar Chart for Subject Performance */}
                    <div className="bg-white p-5 m-3 max-w-lg h-1/2 w-full">
                        <h3>Average Performance by Subject</h3>
                        <Bar data={subjectPerformanceData} />
                    </div>
                </div>
            </div>
        </>
    );
};

export default AdminStudentPerformance;
