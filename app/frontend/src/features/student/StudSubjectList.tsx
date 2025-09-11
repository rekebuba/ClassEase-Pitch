import PropTypes from "prop-types";
import React, { useEffect, useState } from "react";
import { toast } from "sonner";

export function SubjectList({
  studentAssessment,
  student,
  toggleAssessment,
  assessmentSummary,
}) {
  return (
    <section className="table-section">
      <table className="data-table">
        <thead>
          <tr>
            <th>No.</th>
            <th>Subject</th>
            <th>Sem I Total</th>
            <th>Sem I Rank</th>
            <th>Sem II Total</th>
            <th>Sem II Rank</th>
            <th>Average Total</th>
            <th>Average Rank</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {studentAssessment &&
            studentAssessment.assessment &&
            studentAssessment.assessment.map((assessment, index) => {
              const { subject, avg_total, avg_rank, semI, semII } = assessment;
              // Compute averages; adjust logic if necessary
              return (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{subject}</td>
                  <td>{semI.total !== null ? semI.total : "-"}</td>
                  <td>{semI.rank !== null ? semI.rank : "-"}</td>
                  <td>{semII.total !== null ? semII.total : "-"}</td>
                  <td>{semII.rank !== null ? semII.rank : "-"}</td>
                  <td>{avg_total}</td>
                  <td>{avg_rank}</td>
                  <td>
                    <button
                      className="detail-btn"
                      onClick={() => {
                        assessmentSummary({
                          ...student,
                          subject_id: assessment.subject_id,
                        });
                        toggleAssessment();
                      }}
                    >
                      Detail
                    </button>
                  </td>
                </tr>
              );
            })}
          <tr>
            {studentAssessment && studentAssessment.summary && (
              <td colSpan="9" className="bg-gray-100 py-4">
                <div className="flex justify-between items-center px-6 mr-28">
                  {/* Total Section */}
                  <div className="text-lg font-semibold text-gray-700">
                    Total
                  </div>
                  {studentAssessment.summary.semesters.map(
                    (semester, index) => (
                      <React.Fragment key={index}>
                        {/* Semester I Section */}
                        <div className="text-center">
                          <div className="text-sm font-medium text-gray-600">
                            Semester {semester.semester}
                          </div>
                          <div className="text-lg font-bold text-gray-800">
                            {semester.semester_average}
                          </div>
                          <div className="text-sm text-gray-500">
                            Rank: {semester.semester_rank}
                          </div>
                        </div>
                      </React.Fragment>
                    ),
                  )}

                  {/* Average Section */}
                  <div className="text-center">
                    <div className="text-sm font-medium text-gray-600">
                      Average
                    </div>
                    <div className="text-lg font-bold text-green-600">
                      {studentAssessment.summary.final_score}
                    </div>
                    <div className="text-sm text-gray-500">
                      Rank: {studentAssessment.summary.final_rank}
                    </div>
                  </div>
                </div>

                <div className="flex justify-between items-center px-6 mr-28 mt-5">
                  {/* status */}
                  <div className="text-lg font-semibold text-gray-700">
                    Academic Status:{" "}
                    <span className="text-lg font-bold text-green-600">
                      Pending
                    </span>
                  </div>
                </div>
              </td>
            )}
          </tr>
        </tbody>
      </table>
    </section>
  );
}

/**
 * Component for displaying the list of subjects for a student.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleAssessment - Function to toggle the assessment view.
 * @param {Object} props.assessmentSummary - Summary of the student's assessments.
 * @returns {JSX.Element} The rendered component.
 *
 * @example
 * <StudentSubjectList
 *   toggleAssessment={toggleAssessmentFunction}
 *   assessmentSummary={assessmentSummaryObject}
 * />
 *
 * @typedef {Object} Alert
 * @property {string} type - The type of alert (e.g., "warning", "success").
 * @property {string} message - The alert message.
 * @property {boolean} show - Whether the alert is visible.
 *
 * @typedef {Object} Student
 * @property {string} name - The name of the student.
 * @property {number} id - The ID of the student.
 */
const StudentSubjectList = ({ toggleAssessment, assessmentSummary }) => {
  const [selectedSemester, setSelectedSemester] = useState(1);
  const [gradeAssigned, setGradeAssigned] = useState([]);
  const [selectedGrade, setSelectedGrade] = useState(
    gradeAssigned.length > 0 ? gradeAssigned[0] : null,
  );
  const [allSubjects, setAllSubjects] = useState([]);
  const [student, setStudent] = useState({});

  /**
   * @function handleSearch
   * @description Handles the search for student scores based on the selected grade and semester.
   * @async
   * @returns {Promise<void>} A promise that resolves when the search is complete.
   * @throws {Error} An error if the search fails.
   * @throws {string} An error message if the search fails.
   * @throws {Object[]} An array of subjects if the search is successful.
   */
  const handleSearch = async () => {
    try {
      const response = await api.get("/student/score", {
        params: {
          grade: selectedGrade,
          semester: selectedSemester,
        },
      });

      setAllSubjects(response.data["student_assessment"]);
      setStudent(response.data["student"]);
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
      setAllSubjects([]);
      setStudent({});
    }
  };

  /**
   * @function handleSemesterChange
   * @description Handles the change in semester selection.
   * @param {Event} e - The semester change event.
   * @returns {void}
   */
  const handleSemesterChange = (e) => {
    setSelectedSemester(parseFloat(e.target.value));
  };

  /**
   * @function handleGradeChange
   * @description Handles the change in grade selection.
   * @returns {void}
   */
  const handleGradeChange = (e) => {
    setSelectedGrade(parseFloat(e.target.value));
  };

  /**
   * @hook useEffect
   * @description Fetches the assigned grade when the component mounts.
   */
  useEffect(() => {
    /**
     * @function fetchAssignedGrade
     * @description Fetches the assigned grade for the student.
     * @async
     * @returns {Promise<void>} A promise that resolves when the grade is fetched.
     * @throws {Error} An error if the grade fetch fails.
     * @throws {string} An error message if the grade fetch fails.
     * @throws {number[]} An array of assigned grades if the fetch is successful.
     */
    const fetchAssignedGrade = async () => {
      try {
        const response = await api.get("/student/assigned_grade");
        setGradeAssigned(response.data["grade"]);
        setSelectedGrade(response.data["grade"][0]);
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
    fetchAssignedGrade();
  }, []);

  return (
    <div className="dashboard-container">
      <section className="admin-filters">
        <div className="filter-group">
          <label htmlFor="grade">Grade:</label>
          <select id="grade" value={selectedGrade} onChange={handleGradeChange}>
            {gradeAssigned.map((grade) => (
              <option key={grade} value={grade}>
                Grade {grade}
              </option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label htmlFor="semester">Semester:</label>
          <select
            id="semester"
            value={selectedSemester}
            onChange={handleSemesterChange}
          >
            {[1, 2].map((semester) => (
              <option key={semester} value={semester}>
                Semester {semester}
              </option>
            ))}
          </select>
        </div>
        <button className="filter-group-search" onClick={handleSearch}>
          Search
        </button>
      </section>
      <SubjectList
        student={student}
        toggleAssessment={toggleAssessment}
        assessmentSummary={assessmentSummary}
      />
    </div>
  );
};
SubjectList.propTypes = {
  studentAssessment: PropTypes.object,
  student: PropTypes.shape({
    year: PropTypes.string,
    grade: PropTypes.string,
    semester: PropTypes.string,
  }),
  toggleAssessment: PropTypes.func.isRequired,
  assessmentSummary: PropTypes.func.isRequired,
};

export default StudentSubjectList;
