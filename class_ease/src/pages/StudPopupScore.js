import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';

const PopupScore = ({ isOpen, toggleAssessment, studentData }) => {
    const [assessmentData, setAssessmentData] = useState([]);

    useEffect(() => {
        if (studentData.assessment) {
            setAssessmentData(studentData.assessment);
        }
    }, [studentData.assessment]);

    console.log("Student Score: ", studentData);
    console.log("assessment score: ", assessmentData);

    const calculateTotal = () => {
        if (assessmentData.length === 0) return 'N/A';
        const totalScore = assessmentData.reduce((acc, assessment) => acc + (assessment.score || 0), 0);
        return totalScore;
    };

    return (
        <div className={`popup-table-overlay ${isOpen ? "open" : "close"}`}>
            <div className="popup-table">
                <div className="close-popup" >
                    <button onClick={() => {
                        toggleAssessment();
                    }}
                    ><FaTimes size={15} /></button>
                </div>
                <h3>{studentData.subject}</h3>
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
    );
};

export default PopupScore;
