import { getTeachersOptions } from "@/client/@tanstack/react-query.gen";
import { teacherBasicInfoColumns } from "@/components/data-table/manage-teachers/columns";
import { ManageTeacherTable } from "@/components/data-table/manage-teachers/manage-teachers-tabel";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Users } from "lucide-react";

export const Route = createFileRoute("/admin/manage-teachers/")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getTeachersOptions({
          query: { q: "" },
        }),
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();

  const getTeacherQueryConfig = () => ({
    query: { q: "" },
  });

  const { data: teacher } = useQuery({
    ...getTeachersOptions(getTeacherQueryConfig()),
    enabled: !!yearId,
  });

  const handleView = (employeeId: string) => {
    navigate({ to: "/admin/employees/$employeeId", params: { employeeId } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Teacher Management
                </CardTitle>
                <CardDescription>
                  Review and manage all teacher Management in one place
                </CardDescription>
              </div>
              <Button
                onClick={() => {}}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                New Application
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <ManageTeacherTable
              columns={teacherBasicInfoColumns(handleView)}
              data={teacher || []}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
