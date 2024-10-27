import React from 'react';

/**
 * Pagination component for navigating through pages.
 *
 * @param {Object} props - The properties object.
 * @param {function} props.handlePreviousPage - Function to handle the action when the previous page button is clicked.
 * @param {number} props.currentPage - The current page number.
 * @param {function} props.handleNextPage - Function to handle the action when the next page button is clicked.
 * @param {Object} props.meta - Metadata object containing pagination details.
 * @param {number} props.meta.total_pages - The total number of pages.
 *
 * @returns {JSX.Element} The Pagination component.
 */
function Pagination({ handlePreviousPage, currentPage, handleNextPage, meta }) {
    return (<div className="pagination-container">
        <button className="pagination-btn" onClick={handlePreviousPage} disabled={currentPage === 1}>
            Previous
        </button>

        <div className="pagination-info">
            <span> Page </span>
            <input type="text" className="pagination-input" defaultValue={currentPage} min={1} max={meta.total_pages} />
            <span> of {meta.total_pages} </span>
        </div>

        <button className="pagination-btn" onClick={handleNextPage} disabled={currentPage === meta.total_pages}>
            Next
        </button>
    </div>);
}

export default Pagination;
