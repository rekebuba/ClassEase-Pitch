import React from 'react';

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
