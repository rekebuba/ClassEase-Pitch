import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Users } from "lucide-react";
import { toast } from "sonner";

import {
  deleteStudentsMutation,
  getStudentsOptions,
  getStudentsQueryKey,
} from "@/client/@tanstack/react-query.gen";
import { studentBasicInfoColumns } from "@/components/data-table/student-registration/columns";
import { StudentRegistrationTable } from "@/components/data-table/student-registration/student-registration-table";
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

import type { StudentBasicInfo } from "@/client/types.gen";

export const Route = createFileRoute("/admin/registration/students")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getStudentsOptions({
          query: { yearId },
        }),
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();
  const getGradesQueryConfig = () => ({
    query: { yearId: yearId! },
  });

  const { data: students } = useQuery({
    ...getStudentsOptions(getGradesQueryConfig()),
    enabled: !!yearId,
  });

  const deleteStudent = useMutation({
    ...deleteStudentsMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getStudentsQueryKey(getGradesQueryConfig()),
      });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const handleView = (studentId: string) => {
    navigate({ to: "/admin/students/$studentId", params: { studentId } });
  };

  const handleDelete = (studentId: string) => {
    deleteStudent.mutate({ query: { student_ids: [studentId] } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Student Registrations
            </h1>
            <p className="text-gray-600 mt-1">
              Manage and review student registration applications
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-lg px-3 py-1">
              {students?.length}
              {" "}
              Total Registrations
            </Badge>
          </div>
        </div>
        {/* Students Table */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Student Registrations
                </CardTitle>
                <CardDescription>
                  Review and manage all student registration applications
                </CardDescription>
              </div>
              <Button
                onClick={() =>
                  navigate({ to: "/admin/registration/new-student" })}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                New Application
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <StudentRegistrationTable<StudentBasicInfo>
              columns={studentBasicInfoColumns(handleView, handleDelete)}
              data={students || []}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
