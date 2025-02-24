import { useState, useEffect, useCallback } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { teacherApi } from '@/api';
import { toast } from "sonner"

/**
 * TeacherUpdateScore component allows teachers to update student scores.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Object} props.student - Data of the student including assessments.
 *
 * @example
 *
 * @returns {JSX.Element} The TeacherUpdateScore component.
 */
const TeacherUpdateScore = ({ student, setStudents }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [updateAssessmentData, setUpdateAssessmentData] = useState([]);
    const [individualAssessment, setIndividualAssessment] = useState({});

    const fetchIndividualAssessment = useCallback(async () => {
        try {
            const res = await teacherApi.getStudentAssessment({
                student_id: student.student_id,
                grade_id: student.grade_id,
                subject_id: student.subject_id,
                section_id: student.section_id,
                semester: student.semester,
                year: student.year,
            });
            if (res.status === 200) {
                const updatedData = { ...student, ...res.data };
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
    }, [student]);

    useEffect(() => {
        if (Object.keys(student).length === 0) {
            return;
        }
        fetchIndividualAssessment();
    }, [student, fetchIndividualAssessment]);

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
    const handleSave = async (e) => {
        e.preventDefault();
        try {
            const res = await teacherApi.updateScore({ student_data: student, assessments: updateAssessmentData });
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
        await fetchIndividualAssessment();
        await setStudents(e);
    };

    const calculateTotalScore = (assessments) => {
        return parseFloat(assessments.reduce((total, item) => total + item.score, 0).toFixed(2));
    };

    return (
        <>
            <form action="" onSubmit={(e) => handleSave(e)}>
                <div className="flex justify-between items-center p-2">
                    <h3 className='text-center text-lg font-bold'>{student.name} {student.father_name} ({student.student_id})</h3>
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
                <div className='mt-1 flex justify-between'>
                    {isEditing ?
                        <Button
                            type="button"
                            variant="destructive"
                            className="min-w-16"
                            onClick={() => {
                                setIsEditing(false);
                                setUpdateAssessmentData([]);
                            }}
                            disabled={!isEditing}>
                            Cancel
                        </Button>
                        :
                        <Button
                            type="button"
                            variant="default"
                            className="min-w-16"
                            onClick={handleEdit}
                            disabled={isEditing}>
                            Edit
                        </Button>
                    }<Button
                        type="submit"
                        style={{ pointerEvents: 'auto' }}
                        className={`min-w-16 ${isEditing ? 'bg-green-600 hover:bg-opacity-50' : 'bg-gray-400 opacity-50 cursor-not-allowed'}`}
                        disabled={!isEditing}>
                        Save
                    </Button>
                </div>
            </form>
        </>
    );
};

export default TeacherUpdateScore;
