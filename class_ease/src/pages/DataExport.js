import React, { useState } from 'react';
import Papa from 'papaparse'; // For CSV parsing
import jsFileDownload from 'js-file-download'; // For CSV download
import './styles/AdminDashboard.css';
import api from "../services/api";


const DataExport = ({ selectedGrade, selectedYear, showAlert }) => {
    const [studentData, setStudentData] = useState([]);

    const handleSubmit = async () => {
        console.log(selectedGrade);
        console.log(selectedYear);
        try {
            const response = await api.get(`/admin/manage/students?grade=${selectedGrade}&year=${selectedYear}`);
            setStudentData(response.data);
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            } else {
                showAlert("warning", "An unexpected error occurred.");
            }
            return;
        }
        exportCSV();
    };

    // Convert JSON to CSV and trigger download
    const exportCSV = () => {
        const csv = Papa.unparse(studentData); // Convert JSON to CSV
        jsFileDownload(csv, 'students.csv'); // Trigger file download
    };

    return (
        <div className="data-export-import">
            {/* Export Section */}
            <div className="export-section">
                <button onClick={handleSubmit} className="btn btn-primary">
                    Export CSV
                </button>
            </div>
        </div>
    );
};

export default DataExport;
