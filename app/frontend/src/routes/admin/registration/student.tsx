import { getStudentsOptions } from "@/client/@tanstack/react-query.gen";
import { StudentDetailDialog, StudentStatusBadge } from "@/components";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { StudentApplication } from "@/lib/api-validation";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  AlertTriangle,
  CheckCircle,
  Eye,
  Heart,
  Mail,
  MapPin,
  Phone,
  Users,
} from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/admin/registration/student")({
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

  const getInitials = (firstName: string, fatherName: string) => {
    return `${firstName.charAt(0)}${fatherName.charAt(0)}`.toUpperCase();
  };

  const calculateAge = (dateOfBirth: string) => {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
      age--;
    }
    return age;
  };

  const getGradeLevel = (grade: string) => {
    const gradeMap: Record<string, string> = {
      KG: "KG",
      "Grade 1": "1st",
      "Grade 2": "2nd",
      "Grade 3": "3rd",
      "Grade 4": "4th",
      "Grade 5": "5th",
      "Grade 6": "6th",
      "Grade 7": "7th",
      "Grade 8": "8th",
      "Grade 9": "9th",
      "Grade 10": "10th",
      "Grade 11": "11th",
      "Grade 12": "12th",
    };
    return gradeMap[grade] || grade;
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
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[250px]">Student</TableHead>
                    <TableHead>Grade & Academic</TableHead>
                    <TableHead>Family Contact</TableHead>
                    <TableHead>Medical & Special Needs</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Registration</TableHead>
                    <TableHead>Flags</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {students?.map((student) => (
                    <TableRow key={student.id} className="hover:bg-gray-50">
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar className="h-10 w-10">
                            <AvatarImage src={"/placeholder.svg"} />
                            <AvatarFallback>
                              {getInitials(
                                student.firstName,
                                student.fatherName,
                              )}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <div className="font-medium">
                              {student.firstName} {student.fatherName}
                            </div>
                            <div className="text-sm text-gray-500">
                              Age: {calculateAge(student.dateOfBirth)}
                            </div>
                            {student.bloodType && (
                              <div className="text-sm text-gray-500">
                                Blood: {student.bloodType}
                              </div>
                            )}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <Badge className="bg-blue-100 text-blue-800 mb-1">
                            {getGradeLevel(student.grade.grade)}
                          </Badge>
                          {student.isTransfer && (
                            <Badge
                              variant="outline"
                              className="bg-orange-100 text-orange-800 text-xs"
                            >
                              Transfer
                            </Badge>
                          )}
                          <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                            <MapPin className="h-3 w-3" />
                            {student.city}, {student.state}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          <div className="flex items-center gap-1 text-sm">
                            <Phone className="h-3 w-3 text-gray-500" />
                            <span>{student.fatherPhone}</span>
                          </div>
                          <div className="flex items-center gap-1 text-sm">
                            <Phone className="h-3 w-3 text-gray-500" />
                            <span>{student.motherPhone}</span>
                          </div>
                          <div className="flex items-center gap-1 text-sm">
                            <Mail className="h-3 w-3 text-gray-500" />
                            <span className="truncate max-w-[120px]">
                              {student.parentEmail}
                            </span>
                          </div>
                          {student.siblingInSchool && (
                            <Badge variant="outline" className="text-xs">
                              Has Sibling
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {student.hasMedicalCondition && (
                            <Badge
                              variant="destructive"
                              className="text-xs flex items-center gap-1 w-fit"
                            >
                              <Heart className="h-3 w-3" />
                              Medical
                            </Badge>
                          )}
                          {student.hasDisability && (
                            <Badge
                              variant="destructive"
                              className="text-xs flex items-center gap-1 w-fit"
                            >
                              <AlertTriangle className="h-3 w-3" />
                              Disability
                            </Badge>
                          )}
                          {!student.hasMedicalCondition &&
                            !student.hasDisability && (
                              <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1 w-fit">
                                <CheckCircle className="h-3 w-3" />
                                Healthy
                              </Badge>
                            )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <StudentStatusBadge status={student.status} />
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">
                          {formatDate(student.createdAt)}
                        </div>
                        {student.isTransfer && student.previousSchool && (
                          <div className="text-xs text-gray-500">
                            From: {student.previousSchool}
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-col gap-1">
                          {student.isTransfer && (
                            <Badge variant="outline" className="text-xs">
                              Transfer
                            </Badge>
                          )}
                          {(student.hasMedicalCondition ||
                            student.hasDisability) && (
                            <Badge
                              variant="destructive"
                              className="text-xs flex items-center gap-1"
                            >
                              <AlertTriangle className="h-3 w-3" />
                              Needs Attention
                            </Badge>
                          )}
                          {!student.hasMedicalCondition &&
                            !student.hasDisability &&
                            !student.isTransfer && (
                              <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1">
                                <CheckCircle className="h-3 w-3" />
                                Standard
                              </Badge>
                            )}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="outline"
                          size="sm"
                          className="flex items-center gap-1"
                        >
                          <Eye className="h-4 w-4" />
                          View Details
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
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
