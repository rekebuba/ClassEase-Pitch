import { Layout } from "@/components";
import { Shell } from "@/components/shell";
import { StudentsTable } from "@/components/data-table/data-table-students"

interface SearchParams {
  [key: string]: string | string[] | undefined;
}
interface IndexPageProps {
  searchParams: Promise<SearchParams>;
}

const AdminManageStudents = () => {
  return (
    <Layout role="admin">

      <div className="container mx-auto py-5">
        <Shell className="gap-2">
          <StudentsTable />
        </Shell>

      </div>
    </Layout>
  );
};

export default AdminManageStudents;
function useEffect(arg0: () => void, arg1: URLSearchParams[]) {
  throw new Error("Function not implemented.");
}
