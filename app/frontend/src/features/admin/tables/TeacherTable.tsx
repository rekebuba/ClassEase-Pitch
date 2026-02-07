import { DataTable } from "./data-table";
import { teacherColumn } from "./teacherColumns";

function TeacherTable({ data }) {
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={teacherColumn} data={data} />
    </div>
  );
}

export default TeacherTable;
