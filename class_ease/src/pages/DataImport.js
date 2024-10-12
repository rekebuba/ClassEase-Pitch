import React, { useState } from 'react';
import Papa from 'papaparse'; // For CSV parsing
import jsFileDownload from 'js-file-download'; // For CSV download
import './styles/AdminDashboard.css';

const DataImport = () => {
    const [uploadedData, setUploadedData] = useState([]);
    const [uploadError, setUploadError] = useState('');

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

    // Handle CSV file upload and parsing
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            complete: (result) => {
                if (result.errors.length > 0) {
                    setUploadError('Error in CSV format');
                    return;
                }
                setUploadedData(result.data); // Parsed CSV data
                setUploadError(''); // Clear any previous errors
            },
            error: () => {
                setUploadError('File reading error');
            }
        });
    };

    // Export data as PDF (Example: using a simple library like jsPDF)
    const exportPDF = async () => {
        const { jsPDF } = await import('jspdf'); // Dynamic import
        const doc = new jsPDF();

        // Add content to PDF (simple table)
        doc.text('Student Data', 20, 10);
        studentData.forEach((student, index) => {
            doc.text(`${student.name} - Grade: ${student.grade} - Age: ${student.age}`, 20, 20 + index * 10);
        });

        doc.save('students.pdf'); // Download the PDF
    };

    return (
        <div className="data-export-import">
            <h2>Data Export / Import</h2>

            {/* Export Section */}
            <div className="export-section">
                <h3>Export Data</h3>
                <button onClick={exportCSV} className="btn btn-primary">
                    Export CSV
                </button>
                <button onClick={exportPDF} className="btn btn-secondary">
                    Export PDF
                </button>
            </div>

            {/* Import Section */}
            <div className="import-section">
                <h3>Bulk Upload (CSV)</h3>
                <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="file-input"
                />
                {uploadError && <p className="error-text">{uploadError}</p>}

                {/* Display uploaded data (for demo purposes) */}
                {uploadedData.length > 0 && (
                    <div className='uploaded-data'>
                        <h4>Uploaded Data Preview:</h4>
                        <ul>
                            {uploadedData.map((item, index) => (
                                <li key={index}>
                                    {item.name} - Grade: {item.grade} - Age: {item.age}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DataImport;
