import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { useEffect, useState } from "react";
import { Bar, Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  ArcElement,
);

/**
 * ExamAssessmentReports component renders the exam assessment reports for students.
 * It displays two charts: one for subject scores comparison and another for progress tracking over time.
 *
 * @example
 * const subjectSummary = [
 *   { subject: 'Math', subject_average: 85, semester: 'Fall 2021' },
 *   { subject: 'Science', subject_average: 90, semester: 'Fall 2021' },
 * ];
 * <ExamAssessmentReports subjectSummary={subjectSummary} />
 */
function ExamAssessmentReports({ subjectSummary }) {
  const [studentPerformance, setStudentPerformance] = useState({
    subjects: [],
    scores: [],
    timePeriod: [],
    progress: [
      { semester: "", score: null },
      { semester: "", score: null },
      { semester: "", score: null },
    ],
  });

  const barData = {
    labels: studentPerformance.subjects,
    datasets: [
      {
        label: "Subject Scores",
        data: studentPerformance.scores,
        backgroundColor: [
          "rgba(75, 192, 192, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 99, 132, 0.6)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const lineData = {
    labels: studentPerformance.timePeriod,
    datasets: [
      {
        label: "Progress Over Time",
        data: studentPerformance.progress.map(p => p.score),
        fill: false,
        backgroundColor: "rgba(75,192,192,0.6)",
        borderColor: "rgba(75,192,192,1)",
        tension: 0.1,
      },
    ],
  };

  /**
   * Updates the student performance state when the subject summary changes.
   * @param {Array} subjectSummary - An array of subject summary objects.
   * @param {string} subjectSummary[].subject - The name of the subject.
   * @param {number} subjectSummary[].subject_average - The average score for the subject.
   * @param {string} subjectSummary[].semester - The semester for the subject.
   * @returns {void}
   */
  useEffect(() => {
    if (
      subjectSummary !== undefined
      && Object.keys(subjectSummary).length > 0
    ) {
      const subjects = subjectSummary.map(subject => subject.subject);
      const scores = subjectSummary.map(subject => subject.subject_average);
      const timePeriod = subjectSummary.map(subject => subject.semester);
      const progress = subjectSummary.map(subject => ({
        semester: subject.semester,
        score: subject.subject_average,
      }));

      setStudentPerformance({
        ...studentPerformance,
        subjects,
        scores,
        progress,
        timePeriod,
      });
    }
  }, [subjectSummary]);

  return (
    <div className="exam-assessment-reports">
      <div className="admin-dashboard-graph">
        <div className="chart-container">
          <div className="chart-card">
            <h4>Subject Scores Comparison</h4>
            <Bar
              data={barData}
              options={{
                responsive: true,
                plugins: {
                  legend: { display: true },
                  title: { display: true, text: "Scores per Subject" },
                },
              }}
            />
          </div>
          <div className="chart-card">
            <h4>Progress Tracking Over Time</h4>
            <Line
              data={lineData}
              options={{
                responsive: true,
                plugins: {
                  legend: { display: true },
                  title: { display: true, text: "Progress Over Time" },
                },
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExamAssessmentReports;
