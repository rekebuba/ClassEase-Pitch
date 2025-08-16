import { useState, useEffect } from "react";
import { sharedApi } from "@/api";
import { toast } from "sonner";
import ExamAssessmentReports from "./AdminExamAssessmentReports";
import CollapsibleTable from "./CollapsibleTable";

/**
 * StudentProfile component displays a detailed profile of a student including their personal information and performance overview.
 *
 * @component
 * @param {Object} props - The properties object.
 * @param {Object} props.student - An object containing the summary of the student's profile.
 *
 * @returns {JSX.Element} The rendered StudentProfile component.
 */
const AdminStudentProfile = ({ student }) => {
  const [allSubjects, setAllSubjects] = useState([]);
  const [studentAssessment, setStudentAssessment] = useState([]);
  const [studentReport, setStudentReport] = useState([]);

  /**
   * @function calculateAge
   * @param {string} birthday - The date of birth of the student in 'YYYY-MM-DD' format.
   * @returns {number} The age of the student.
   * @description Calculates the age of the student based on their date of birth.
   */
  function calculateAge(birthday) {
    // birthday should be in the format 'YYYY-MM-DD'
    const birthDate = new Date(birthday);
    const today = new Date();

    return today.getFullYear() - birthDate.getFullYear();
  }

  useEffect(() => {
    /**
     * @function lodeStudentSubjectList
     * @description Loads the list of subjects for the student.
     * @async
     * @returns {Promise<void>} The response data.
     * @throws {error} The error that was caught
     */
    const lodeStudentSubjectList = async () => {
      try {
        if (student !== undefined && Object.keys(student).length > 0) {
          const response = await sharedApi.getStudentAssessment({
            student_id: student.student_id,
            grade_id: student.grade_id,
            section_id: student.section_id,
            year: student.year,
          });
          setStudentAssessment(response.data.assessment);
          setStudentReport(response.data.summary);
        }
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data["error"]
        ) {
          toast.error(error.response.data["error"], {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        } else {
          toast.error("An unexpected error occurred.", {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        }
      }
    };
    lodeStudentSubjectList();
  }, [student]);

  return (
    <>
      <div className="flex mb-5">
        <div className="mr-5">
          <img
            className=" w-[150px] h-[150px] object-cover rounded-[50%]"
            src={student.pictureUrl}
            alt="Student"
          />
        </div>
        <div className="flex-1">
          <h2 className="mt-0 mb-2.5 mx-0">
            {student.name} {student.father_name}{" "}
            {student.grand_father_name}{" "}
          </h2>
          <p>Age: {calculateAge(student.date_of_birth)}</p>
          <p>Grade: {student.grade}</p>
          <p style={{ margin: 0 }}>Section: {student.section}</p>
        </div>
      </div>

      <div className="mb-3">
        <h3>Performance Overview</h3>
        <ExamAssessmentReports subjectSummary={allSubjects} />
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-bold mt-5">
            <span>{`Academic Year: ${student.year}`}</span>
            <span className="ml-5">{`Grade: ${student.grade}`}</span>
            <span className="ml-5">{`Semester: ${student.semester}`}</span>
          </h3>
        </div>
        {studentAssessment && (
          <CollapsibleTable
            studentAssessment={studentAssessment}
            studentReport={studentReport}
          />
        )}
      </div>
    </>
  );
};

export default AdminStudentProfile;
