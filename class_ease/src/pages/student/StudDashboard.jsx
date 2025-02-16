import { useState, useEffect } from "react";
import { StudentHeader, StudentPanel } from "@/components/layout";
import { StudentPopupScore, StudentSubjectList, StudentEventPanel, StudentScorePanel } from "@/features/student";
import { studentApi } from "@/api";
import { toast } from "sonner"
import { Toaster } from '@/components/ui/sonner';
import '../../styles/StudDashboard.css';
import '../../styles/Dashboard.css';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button";
import { FaTimes } from "react-icons/fa";
import { CheckCircle } from "lucide-react";
/**
 * StudentDashboard component renders the main dashboard for students.
 * It includes the student panel, subject list, and a popup for assessment scores.
 *
 * @component
 * @example
 * return (
 *   <StudentDashboard />
 * )
 *
 * @returns {JSX.Element} The rendered student dashboard component.
 *
 * @function
 * @name StudentDashboard
 * @description
 * - Manages the state for assessment popup visibility and student summary.
 * - Toggles the assessment popup visibility.
 * - Closes the assessment popup.
 * - Updates the student summary with provided data.
 */
const StudentDashboard = () => {
  const [isAssesOpen, setIsAssesOpen] = useState(false);
  const [studentSummary, setStudentSummary] = useState({});
  const [yearlyScore, setYearlyScore] = useState([]);


  useEffect(() => {
    const fetchStudent = async () => {
      try {
        const response = await studentApi.getYearlyScore();
        if (response.data) {
          setYearlyScore(response.data.score);
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data['error']) {
          toast.error(error.response.data['error'], {
            description: "Please try again later, if the problem persists, contact the administrator.",
            style: { color: 'red' }
          });
        } else {
          toast.error("An unexpected error occurred.", {
            description: "Please try again later, if the problem persists, contact the administrator.",
            style: { color: 'red' }
          });
        }
      }
    };

    fetchStudent();
  }, []);

  const toggleAssessment = (value) => {
    setIsAssesOpen(value);
  };


  /**
   * @function closeAssessment
   * @description Closes the assessment popup.
   * @returns {void}
   */
  const closeAssessment = () => {
    setIsAssesOpen(false);
  };

  /**
   * @function summary
   * @param {object} data - The summary of the student's assessments.
   * @description Updates the student summary with provided data.
   * @returns {void}
   */
  const summary = (data) => {
    setStudentSummary(data);
  };

  return (
    <div className="min-h-screen flex overflow-hidden flex-col">
      <StudentHeader />
      <div className="flex flex-1 scroll-m-0">
        <StudentPanel />
        <main className="p-10 mt-[4.6rem] ml-[11rem] bg-gray-50">

          <div className="flex space-x-10">
            <StudentEventPanel />
            <StudentScorePanel yearlyScore={yearlyScore} isAssesOpen={toggleAssessment} />
          </div>
          {isAssesOpen && (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
              <Card className={`bg-white p-2 rounded-lg shadow-lg w-[45rem] transform transition-all duration-300 ease-out ${isAssesOpen ? "opacity-100 scale-100" : "opacity-0 scale-90"}`}>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <h3 className='text-center text-lg font-bold'>student Score</h3>
                    <Button
                      className='bg-opacity-0 text-black hover:bg-opacity-10 hover:text-red-400 hover:scale-150'
                      onClick={() => toggleAssessment(false)}
                    >
                      <FaTimes size={24} />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="p-4">
                  <div className="mt-3 space-y-2">
                    {/* detailed student yearly Score */}
                    {yearlyScore &&
                      Object.keys(yearlyScore).length > 0 &&
                      Object.entries(yearlyScore).map(([key, item]) => (
                        <div key={key}>
                          {/* Parent container for Grade */}
                          <div className="flex justify-between border-b-2 border-gray-100 pb-2">
                            <p>Grade {item.grade}</p>
                            <p className="flex items-center">
                              {item.final_score} % <CheckCircle className="h-5 w-5 text-green-500 ml-1" />
                            </p>
                          </div>

                          {/* Nested iteration over semesters */}
                          {item && Object.keys(item.semester).length > 0 && item.semester.map((sem, index) => (
                            <div key={index} className="flex justify-between border-b-2 border-gray-100 pb-2 ml-4">
                              <p>Semester {sem.semester}</p>
                              <p className="flex items-center">{sem.average} %</p>
                            </div>
                          ))}
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* <StudentSubjectList
            toggleAssessment={toggleAssessment}
            assessmentSummary={summary}
          />
          <StudentPopupScore
            isAssesOpen={isAssesOpen}
            closeAssessment={closeAssessment}
            assessmentSummary={studentSummary}
          /> */}
          <Toaster />
        </main>
      </div>
    </div>
  );
};
export default StudentDashboard;
