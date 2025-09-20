import {
  deleteEmployeesMutation,
  getEmployeesOptions,
  getEmployeesQueryKey,
} from "@/client/@tanstack/react-query.gen";
import { employeeBasicInfoColumns } from "@/components/data-table/employee-registration/columns";
import { EmployeeRegistrationTable } from "@/components/data-table/employee-registration/employee-registration-table";
import { Badge } from "@/components/ui/badge";
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
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Users } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/registration/employees")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getEmployeesOptions({
          query: { q: "" },
        }),
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();

  const getEmployeesQueryConfig = () => ({
    query: { q: "" },
  });

  const { data: employees } = useQuery({
    ...getEmployeesOptions(getEmployeesQueryConfig()),
    enabled: !!yearId,
  });

  const deleteEmployee = useMutation({
    ...deleteEmployeesMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getEmployeesQueryKey(getEmployeesQueryConfig()),
      });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const handleView = (employeeId: string) => {
    navigate({ to: "/admin/employees/$employeeId", params: { employeeId } });
  };

  const handleDelete = (employeeId: string) => {
    deleteEmployee.mutate({ query: { employee_ids: [employeeId] } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Employees Applications
            </h1>
            <p className="text-gray-600 mt-1">
              Manage and Review Employees Applications
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-lg px-3 py-1">
              {employees?.length} Total Applications
            </Badge>
          </div>
        </div>

        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Employee Applications
                </CardTitle>
                <CardDescription>
                  Review and manage all employee applications in one place
                </CardDescription>
              </div>
              <Button
                onClick={() =>
                  navigate({ to: "/admin/registration/new-employee" })
                }
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                New Application
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <EmployeeRegistrationTable
              columns={employeeBasicInfoColumns(handleView, handleDelete)}
              data={employees || []}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
