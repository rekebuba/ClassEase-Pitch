import { StudentsTable } from "@/components/data-table/data-table-students";
import { Shell } from "@/components/shell";

type SearchParams = {
  [key: string]: string | string[] | undefined;
};
type IndexPageProps = {
  searchParams: Promise<SearchParams>;
};

function AdminManageStudents() {
  return (
    <div className="container mx-auto py-5">
      <Shell className="gap-2">
        <StudentsTable />
      </Shell>
    </div>
  );
}

export default AdminManageStudents;
function useEffect(arg0: () => void, arg1: URLSearchParams[]) {
  throw new Error("Function not implemented.");
}
