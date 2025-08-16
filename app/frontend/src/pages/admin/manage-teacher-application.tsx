"use client";

import { detailTeachersApplications, fetchTeachersApplications } from "@/api";
import { TeacherDetailDialog, TeacherStatusBadge } from "@/components";
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
import type {
  TeacherApplication,
  TeacherApplicationWithDetails,
} from "@/lib/api-validation";
import {
  AlertTriangle,
  Award,
  Calendar,
  CheckCircle,
  Clock,
  Eye,
  GraduationCap,
  Mail,
  MapPin,
  Phone,
  Users,
  XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";

export default function ManageTeachersApplication() {
  const [teachers, setTeachers] = useState<TeacherApplication[]>([]);
  const [selectedTeacher, setSelectedTeacher] =
    useState<TeacherApplicationWithDetails | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  useEffect(() => {
    const fetchTeacherApplications = async () => {
      const response = await fetchTeachersApplications();
      setTeachers(response);
    };
    fetchTeacherApplications().catch((error) => {
      console.error("Failed to fetch teacher applications:", error);
    });
  }, []);

  const handleViewDetails = async (teacher: TeacherApplication) => {
    const detail = await detailTeachersApplications(teacher.id);
    setSelectedTeacher({
      ...teacher,
      ...detail,
    });
    setIsDetailDialogOpen(true);
  };

  const handleStatusChange = (
    teacherId: string,
    newStatus: TeacherApplication["status"],
  ) => {
    setTeachers((prev) =>
      prev.map((teacher) =>
        teacher.id === teacherId ? { ...teacher, status: newStatus } : teacher,
      ),
    );
  };

  const getStatusCounts = () => {
    return teachers.reduce(
      (acc, teacher) => {
        acc[teacher.status] = (acc[teacher.status] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>,
    );
  };

  const statusCounts = getStatusCounts();

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  };

  const getExperienceLevel = (experience: string) => {
    const experienceMap = {
      "0": "New",
      "1-2": "Entry",
      "3-5": "Junior",
      "6-10": "Mid",
      "11-15": "Senior",
      "16-20": "Expert",
      "20+": "Veteran",
    };
    return (
      experienceMap[experience as keyof typeof experienceMap] || experience
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Teacher Applications
            </h1>
            <p className="text-gray-600 mt-1">
              Manage and review teacher applications
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-lg px-3 py-1">
              {teachers.length} Total Applications
            </Badge>
          </div>
        </div>

        {/* Status Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <Clock className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">
                {statusCounts.pending || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Under Review
              </CardTitle>
              <Eye className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {statusCounts["under-review"] || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Interview Scheduled
              </CardTitle>
              <Calendar className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">
                {statusCounts["interview-scheduled"] || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Approved</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {statusCounts.approved || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Rejected</CardTitle>
              <XCircle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {statusCounts.rejected || 0}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Teachers Table */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Teacher Applications
                </CardTitle>
                <CardDescription>
                  Review and manage all teacher applications in one place
                </CardDescription>
              </div>
              <Button
                onClick={() => {
                  // Navigate to new application page
                  window.location.href = "/admin/teacher/registration/new";
                }}
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
                    <TableHead className="w-[250px]">Applicant</TableHead>
                    <TableHead>Position</TableHead>
                    <TableHead>Experience</TableHead>
                    <TableHead>Education</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Applied</TableHead>
                    <TableHead>Flags</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {teachers && teachers.length > 0 ? (
                    teachers.map((teacher) => (
                      <TableRow key={teacher.id} className="hover:bg-gray-50">
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <Avatar className="h-10 w-10">
                              <AvatarImage
                                src={teacher.profilePhoto || "/placeholder.svg"}
                              />
                              <AvatarFallback>
                                {getInitials(
                                  teacher.firstName,
                                  teacher.fatherName,
                                )}
                              </AvatarFallback>
                            </Avatar>
                            <div>
                              <div className="font-medium">
                                {teacher.firstName} {teacher.fatherName}
                              </div>
                              <div className="text-sm text-gray-500 flex items-center gap-1">
                                <Mail className="h-3 w-3" />
                                {teacher.personalEmail}
                              </div>
                              <div className="text-sm text-gray-500 flex items-center gap-1">
                                <Phone className="h-3 w-3" />
                                {teacher.primaryPhone}
                              </div>
                              <div className="text-sm text-gray-500 flex items-center gap-1">
                                <MapPin className="h-3 w-3" />
                                {teacher.city}, {teacher.state}
                              </div>
                            </div>
                          </div>
                        </TableCell>

                        <TableCell>
                          <div>
                            <div className="font-medium">
                              {teacher.positionApplyingFor}
                            </div>
                          </div>
                        </TableCell>

                        <TableCell>
                          <div>
                            <Badge variant="outline" className="mb-1">
                              {getExperienceLevel(teacher.yearsOfExperience)}
                            </Badge>
                            <div className="text-sm text-gray-500">
                              {teacher.yearsOfExperience} years
                            </div>
                            {teacher.teachingLicense && (
                              <div className="flex items-center gap-1 text-sm text-green-600">
                                <Award className="h-3 w-3" />
                                Licensed
                              </div>
                            )}
                          </div>
                        </TableCell>

                        <TableCell>
                          <div>
                            <div className="flex items-center gap-1">
                              <GraduationCap className="h-4 w-4 text-gray-500" />
                              <span className="capitalize text-sm font-medium">
                                {teacher.highestDegree.replace("-", " ")}
                              </span>
                            </div>
                            <div className="text-sm text-gray-500">
                              {teacher.university}
                            </div>
                            {teacher.gpa && (
                              <div className="text-sm text-gray-500">
                                GPA: {teacher.gpa}
                              </div>
                            )}
                          </div>
                        </TableCell>

                        <TableCell>
                          <TeacherStatusBadge status={teacher.status} />
                        </TableCell>

                        <TableCell>
                          <div className="text-sm">
                            {formatDate(teacher.applicationDate)}
                          </div>
                        </TableCell>

                        <TableCell>
                          <div className="flex flex-col gap-1">
                            {teacher.hasConvictions && (
                              <Badge
                                variant="destructive"
                                className="text-xs flex items-center gap-1"
                              >
                                <AlertTriangle className="h-3 w-3" />
                                Criminal Record
                              </Badge>
                            )}
                            {teacher.hasDisciplinaryActions && (
                              <Badge
                                variant="destructive"
                                className="text-xs flex items-center gap-1"
                              >
                                <AlertTriangle className="h-3 w-3" />
                                Disciplinary
                              </Badge>
                            )}
                            {!teacher.teachingLicense && (
                              <Badge variant="secondary" className="text-xs">
                                No License
                              </Badge>
                            )}
                            {!teacher.hasConvictions &&
                              !teacher.hasDisciplinaryActions &&
                              teacher.teachingLicense && (
                                <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1">
                                  <CheckCircle className="h-3 w-3" />
                                  Clean
                                </Badge>
                              )}
                          </div>
                        </TableCell>

                        <TableCell className="text-right">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleViewDetails(teacher)}
                            className="flex items-center gap-1"
                          >
                            <Eye className="h-4 w-4" />
                            View Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableCell
                      // colSpan={table.getAllColumns().length}
                      className="h-24 text-center"
                    >
                      No results.
                    </TableCell>
                  )}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Teacher Detail Dialog */}
        <TeacherDetailDialog
          teacher={selectedTeacher}
          isOpen={isDetailDialogOpen}
          onClose={() => {
            setIsDetailDialogOpen(false);
            setSelectedTeacher(null);
          }}
          onStatusChange={handleStatusChange}
        />
      </div>
    </div>
  );
}
