import { useState, useEffect, useCallback } from 'react';
import { FaTimes } from 'react-icons/fa';
import api from '../../services/api';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from "sonner"

/**
 * TeacherPopupUpdateStudentScore component allows teachers to update student scores.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {boolean} props.isOpen - Determines if the popup is open.
 * @param {Function} props.toggleAssessment - Function to toggle the assessment popup.
 * @param {Object} props.studentData - Data of the student including assessments.
 * @param {Array} props.studentData.assessment - Array of assessment objects.
 * @param {string} props.studentData.name - Name of the student.
 * @param {string} props.studentData.father_name - Father's name of the student.
 *
 * @example
 *
 * @returns {JSX.Element} The TeacherPopupUpdateStudentScore component.
 */
const TeacherPopupUpdateStudentScore = ({ isOpen, toggleAssessment, studentData, onSave }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [updateAssessmentData, setUpdateAssessmentData] = useState([]);
    const [individualAssessment, setIndividualAssessment] = useState({});

    const fetchIndividualAssessment = useCallback(async () => {
        try {
            const res = await api.get('/teacher/student/assessment', {
                params: {
                    student_id: studentData.student_id,
                    grade_id: studentData.grade_id,
                    subject_id: studentData.subject_id,
                    section_id: studentData.section_id,
                    semester: studentData.semester,
                    year: studentData.year,
                },
            });
            if (res.status === 200) {
                const updatedData = { ...studentData, ...res.data };
                setIndividualAssessment(updatedData);
            }
        } catch (error) {
            if (error.response?.data?.error) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
    }, [studentData]);

    useEffect(() => {
        if (Object.keys(studentData).length === 0) {
            return;
        }
        fetchIndividualAssessment();
    }, [studentData, fetchIndividualAssessment]);

    /**
     * @function handleScoreChange
     * @description Updates the score of an assessment.
     * @param {number} index - Index of the assessment in the array.
     * @param {number} value - New score value.
     * @returns {void}
     */
    const handleScoreChange = (index, value) => {
        const updatedAssessments = [...updateAssessmentData];
        updatedAssessments[index].score = value;
        setUpdateAssessmentData(updatedAssessments);
    };

    /**
     * @function handleEdit
     * @description Sets the editing mode to true.
     * @returns {void}
     */
    const handleEdit = () => {
        setIsEditing(true);
        const updatedAssessments = individualAssessment.assessment.map((assessment) => ({
            ...assessment,
        }));
        setUpdateAssessmentData(updatedAssessments);
    };

    /**
     * @function handleSave
     * @description Saves the updated assessment data.
     * @returns {void}
     */
    const handleSave = async () => {
        setIsEditing(false);
        try {
            const res = await api.put('/teacher/students/mark_list', { student_data: studentData, assessments: updateAssessmentData });
            if (res.status === 201) {
                const currentTime = new Date().toLocaleString("en-US", {
                    weekday: "long",
                    year: "numeric",
                    month: "long",
                    day: "2-digit",
                    hour: "numeric",
                    minute: "2-digit",
                    hour12: true,
                });
                toast.success(res.data['message'], {
                    description: currentTime,
                    style: { color: 'green' }
                });
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
        // Fetch updated data and pass it to onSave
        await fetchIndividualAssessment();
        onSave(true); // to get the updated student data
    };

    const calculateTotalScore = (assessments) => {
        return parseFloat(assessments.reduce((total, item) => total + item.score, 0).toFixed(2));
    };

    return (
        <div className={`popup-overlay ${isOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container score'>
                <div className="popup-table">
                    <div className="flex justify-between items-center p-2">
                        <h3 className='text-center text-lg font-bold'>{studentData.name} {studentData.father_name} ({studentData.student_id})</h3>
                        <Button
                            className='bg-opacity-0 text-black hover:bg-opacity-10 hover:text-red-400 hover:scale-150'
                            onClick={() => {
                                setIsEditing(false);
                                setUpdateAssessmentData([]);
                                toggleAssessment();
                            }}
                        >
                            <FaTimes size={15} />
                        </Button>
                    </div>
                    <table className='w-full text-left border-collapse'>
                        <thead>
                            <tr className='bg-gray-200'>
                                <th className='p-1.5 overflow-hidden'>Type</th>
                                <th className='p-1.5 overflow-hidden'>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(individualAssessment.assessment && individualAssessment.assessment.length > 0) &&
                                individualAssessment.assessment.map((assessment, index) => (
                                    <tr key={index} className={`text-left bg-${index % 2 === 0 ? 'white' : 'gray-100'} hover:bg-gray-200`}>
                                        <td className='text-left p-2'>{assessment.assessment_type} ( {assessment.percentage}% )</td>
                                        <td>
                                            {isEditing ? (
                                                <Input
                                                    className="w-12 text-center border-solid border-2 border-gray-300"
                                                    id={index}
                                                    value={updateAssessmentData[index].score || ''}
                                                    onChange={(e) => {
                                                        let newScore = parseFloat(e.target.value);
                                                        if (newScore > assessment.percentage) newScore = assessment.percentage;
                                                        handleScoreChange(index, newScore);
                                                    }}>
                                                </Input>
                                            ) : (
                                                assessment.score !== null ? assessment.score : '-'
                                            )}
                                        </td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                    <div className='text-right text-lg p-2'>
                        <h3><strong>Total Score: {individualAssessment.assessment ? calculateTotalScore(individualAssessment.assessment) : 'N/A'} / 100</strong></h3>
                    </div>
                    <div className='popup-table-btn'>
                        {isEditing ?
                            <Button className="bg-red-600 min-w-16 hover:bg-opacity-50"
                                onClick={() => {
                                    setIsEditing(false);
                                    setUpdateAssessmentData([]);
                                }}>
                                Cancel
                            </Button>
                            :
                            <Button className="bg-blue-600 min-w-16 hover:bg-opacity-50" onClick={handleEdit}>
                                Edit
                            </Button>
                        }<Button
                            style={{ pointerEvents: 'auto' }}
                            className={`${isEditing ? 'bg-green-600 min-w-16 hover:bg-opacity-50' : 'bg-gray-400 opacity-50 cursor-not-allowed'}`}
                            disabled={!isEditing}
                            onClick={handleSave}>
                            Save
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TeacherPopupUpdateStudentScore;
