import { DataTable } from "./data-table";
import { courseColumn } from "./courseColumn";

const CourseTable = ({ courses }) => {
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={courseColumn} data={courses} />
    </div>
  );
};

export default CourseTable;
