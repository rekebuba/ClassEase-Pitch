import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';

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
const PopupScore = ({ isAssesOpen, closeAssessment, assessmentSummary }) => {
    const [assessmentData, setAssessmentData] = useState([]);

    /**
     * @hook useEffect
     * @description Sets the assessment data when the assessment summary changes.
     */
    useEffect(() => {
        if (assessmentSummary.assessment) {
            setAssessmentData(assessmentSummary.assessment);
        }
    }, [assessmentSummary.assessment]);

    /**
     * @function calculateTotal
     * @description Calculates the total score of all assessments.
     */
    const calculateTotal = () => {
        if (assessmentData.length === 0) return 'N/A';
        const totalScore = assessmentData.reduce((acc, assessment) => acc + (assessment.score || 0), 0);
        return totalScore;
    };

    return (
        <div className={`popup-overlay ${isAssesOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container score'>
                <div className="popup-table">
                    <div className="close-popup" >
                        <h3>{assessmentSummary.subject}</h3>
                        <button onClick={() => {
                            closeAssessment();
                        }}
                        ><FaTimes size={15} /></button>
                    </div>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>No.</th>
                                <th>Assessment</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(assessmentData && assessmentData.length > 0) &&
                                assessmentData.map((assessment, index) => (
                                    <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                                        <td>{index + 1}</td>
                                        <td>{assessment.assessment_type} ( {assessment.percentage}% )</td>
                                        <td>
                                            {assessment.score || 'N/A'}
                                        </td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                    <div className='total-score'>
                        <h3><strong>Total Score: {calculateTotal()} / 100</strong></h3>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PopupScore;
