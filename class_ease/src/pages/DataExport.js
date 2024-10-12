import React, { useState } from 'react';
import Papa from 'papaparse'; // For CSV parsing
import jsFileDownload from 'js-file-download'; // For CSV download
import './styles/AdminDashboard.css';

const DataExport = () => {
    // Example dummy data
    const studentData = [
        { id: 1, name: 'John Doe', grade: 'A', age: 16 },
        { id: 2, name: 'Jane Smith', grade: 'B', age: 15 },
        { id: 3, name: 'Samuel Johnson', grade: 'C', age: 17 }
    ];

    // Convert JSON to CSV and trigger download
    const exportCSV = () => {
        const csv = Papa.unparse(studentData); // Convert JSON to CSV
        jsFileDownload(csv, 'students.csv'); // Trigger file download
    };

    return (
        <div className="data-export-import">
            {/* Export Section */}
            <div className="export-section">
                <button onClick={exportCSV} className="btn btn-primary">
                    Export CSV
                </button>
            </div>
        </div>
    );
};

export default DataExport;
