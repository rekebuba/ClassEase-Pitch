import { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import { api } from "@/api";
import { toast } from "sonner"
import { Button } from '@/components/ui/button';


/**
 * PopupScore component displays a popup with assessment scores.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {boolean} props.isAssesOpen - Flag to determine if the popup is open.
 * @param {Function} props.closeAssessment - Function to close the popup.
 * @param {Object} props.assessmentSummary - Summary of the assessment.
 * @param {string} props.assessmentSummary.subject - Subject of the assessment.
 * @param {Array} props.assessmentSummary.assessment - Array of assessment objects.
 * @param {string} props.assessmentSummary.assessment[].assessment_type - Type of the assessment.
 * @param {number} props.assessmentSummary.assessment[].percentage - Percentage of the assessment.
 * @param {number} [props.assessmentSummary.assessment[].score] - Score of the assessment.
 *
 * @returns {JSX.Element} The rendered PopupScore component.
 */
const StudentPopupScore = ({ isAssesOpen, closeAssessment, assessmentSummary }) => {
    const [assessmentData, setAssessmentData] = useState({});

    /**
     * @hook useEffect
     * @description Sets the assessment data when the assessment summary changes.
     */
    useEffect(() => {
        const assessmentReport = async () => {
            try {
                const res = await api.get('/student/assessment/detail', {
                    params: {
                        student_id: assessmentSummary.student_id,
                        grade_id: assessmentSummary.grade_id,
                        subject_id: assessmentSummary.subject_id,
                        section_id: assessmentSummary.section_id,
                        year: assessmentSummary.year,
                    },
                });
                if (res.status === 200) {
                    console.log(res.data);
                    setAssessmentData(res.data);
                }
            } catch (error) {
                if (error.response?.data?.error) {
                    toast.error(error.response.data['error'], {
                        description: "Please try again later, if the problem persists, contact the administrator.",
                        style: { color: 'red' }
                    });
                }
            }
        }
        assessmentReport()
    }, [assessmentSummary]);

    const calculateTotalScore = (assessments) => {
        return parseFloat(assessments.reduce((total, item) => total + item.score, 0).toFixed(2));
    };

    return (
        <div className={`popup-overlay ${isAssesOpen ? "open" : "close"}`}>
            <div className='bg-white rounded-md p-5 shadow-slate-400 overflow-auto'>
                <div className="popup-table">
                    <div className="flex justify-between items-center p-2">
                        <h3 className='text-center text-lg font-bold'>History</h3>
                        <Button
                            className='bg-opacity-0 text-black hover:bg-opacity-10 hover:text-red-400 hover:scale-150'
                            onClick={() => {
                                closeAssessment();
                            }}
                        ><FaTimes size={15} /></Button>
                    </div>
                    <div className='flex flex-wrap justify-between p-2 gap-10'>
                        {(assessmentData && Object.entries(assessmentData).length !== 0) &&
                            Object.keys(assessmentData).map((semester) => (
                                <div key={semester} className='flex-1 p-4 w-96 min-w-[250px] border border-gray-300 rounded-lg shadow-md bg-white'>
                                    <h3 className='text-center text-lg font-bold'>Semester {semester}</h3>
                                    <table className='w-full text-left border-collapse'>
                                        <thead>
                                            <tr className='bg-gray-200'>
                                                <th className='p-1.5 overflow-hidden'>No.</th>
                                                <th className='p-1.5 overflow-hidden'>Type</th>
                                                <th className='p-1.5 overflow-hidden'>Score</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {assessmentData[semester].map((assessment, i) => (
                                                <tr key={i} className={`text-left ${i % 2 === 0 ? 'bg-white' : 'bg-gray-100'} hover:bg-gray-200`}>
                                                    <td className="p-2">{i + 1}</td>
                                                    <td className='text-left p-2'>{assessment.assessment_type} ({assessment.percentage}%)</td>
                                                    <td className="p-2">{assessment.score || 'N/A'}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                    <div className='text-right text-lg p-2'>
                                        <h3><strong>Total Score: {assessmentData[semester] ? calculateTotalScore(assessmentData[semester]) : 'N/A'} / 100</strong></h3>
                                    </div>
                                </div>
                            ))
                        }
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StudentPopupScore;
