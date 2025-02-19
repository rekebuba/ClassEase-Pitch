import { useNavigate } from "react-router-dom";
import classEaseHeader from '../../assets/images/ClassEase-header.png';

function StudentHeader() {
    const navigate = useNavigate();

    /**
    * Navigates the user to the home page.
    */
    const goToHome = () => {
        navigate("/");
    };

    return (
        <header className="flex w-full h-[4.6rem] p-2 bg-white shadow border-b border-gray-200 fixed">
            <div className="cursor-pointer flex justify-between flex-shrink-0 align-middle" onClick={goToHome}>
                <img src={classEaseHeader} alt="ClassEase School" className="h-10" />
            </div>
        </header>
    );
}

export default StudentHeader;
