import { courseColumn } from "./courseColumn";
import { DataTable } from "./data-table";

function CourseTable({ courses }) {
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={courseColumn} data={courses} />
    </div>
  );
}

export default CourseTable;
