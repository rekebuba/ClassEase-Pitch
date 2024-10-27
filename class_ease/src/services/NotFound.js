import React from 'react';
import '../styles/notfound.css'


/**
 * NotFound Component
 * 
 * This functional component renders a 404 error message indicating that the requested page was not found.
 * It displays a sad face emoji followed by the text "404, page not found."
 * 
 * @component
 * @example
 * return (
 *   <NotFound />
 * )
 * 
 * @returns {JSX.Element} A JSX element containing the 404 error message.
 */
const NotFound = () => {
    return (
        <div class="container-404">
            <div class="copy-container center-xy">
                <p>
                    😥404, page not found.
                </p>
                <span class="handle"></span>

            </div>
        </div>
    )
};

export default NotFound;
