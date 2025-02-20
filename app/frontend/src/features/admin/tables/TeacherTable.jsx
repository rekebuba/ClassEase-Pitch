import { teacherColumn } from "./teacherColumns"
import { DataTable } from "./data-table"

const TeacherTable = ({ data }) => {
    return (
        <div className="container mx-auto py-10">
            <DataTable columns={teacherColumn} data={data} />
        </div>
    );
}

export default TeacherTable;
