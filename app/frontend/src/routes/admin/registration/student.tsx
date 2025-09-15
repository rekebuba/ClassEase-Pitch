import {
  deleteStudentsMutation,
  getStudentsOptions,
} from "@/client/@tanstack/react-query.gen";
import { StudentBasicInfo } from "@/client/types.gen";
import { StudentDetailDialog } from "@/components";
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
import type { StudentApplication } from "@/lib/api-validation";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Users } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/registration/student")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getStudentsOptions({
          query: { yearId },
        })
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();
  // const [students, setStudents] = useState<StudentBasicInfo[]>(mockStudents);
  const [selectedStudent, setSelectedStudent] =
    useState<StudentApplication | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const {
    data: students,
    isLoading,
    error,
  } = useQuery({
    ...getStudentsOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const deleteStudent = useMutation({
    ...deleteStudentsMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getStudentsOptions(getYearQueryConfig()),
      });
      queryClient.invalidateQueries({
        queryKey: getStudentsOptions().queryKey,
      });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const handleDelete = (yearId: string) => {
    deleteStudent.mutate({ path: { year_id: yearId } });
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
              {students?.length} Total Registrations
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
                  navigate({ to: "/admin/registration/new-student" })
                }
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                New Application
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <StudentRegistrationTable<StudentBasicInfo>
              columns={studentBasicInfoColumns(() => {}, handleDelete)}
              data={students || []}
            />
          </CardContent>
        </Card>
        {/* Student Detail Dialog */}
        <StudentDetailDialog
          student={selectedStudent}
          isOpen={isDetailDialogOpen}
          onClose={() => {
            setIsDetailDialogOpen(false);
            setSelectedStudent(null);
          }}
          onStatusChange={() => {}}
        />
      </div>
    </div>
  );
}
