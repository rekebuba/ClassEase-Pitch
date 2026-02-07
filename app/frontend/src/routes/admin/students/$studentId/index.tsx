import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  AlertTriangle,
  Ban,
  BookOpen,
  Bus,
  CheckCircle,
  Clock,
  FileText,
  GraduationCap,
  Heart,
  Home,
  Info,
  LogOut,
  Mail,
  MapPin,
  Pause,
  Phone,
  User,
  Users,
  XCircle,
} from "lucide-react";
import { toast } from "sonner";

import {
  getStudentOptions,
  getStudentQueryKey,
  updateStudentStatusMutation,
} from "@/client/@tanstack/react-query.gen";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { calculateAge, getInitials } from "@/utils/utils";

import type { StudentApplicationStatusEnum as Status } from "@/client/types.gen";

export const Route = createFileRoute("/admin/students/$studentId/")({
  component: RouteComponent,
  loader: async ({ params }) => {
    await queryClient.ensureQueryData(
      getStudentOptions({
        path: { student_id: params.studentId },
      }),
    );
  },
});

export default function RouteComponent() {
  const studentId = Route.useParams().studentId;
  const navigate = useNavigate();

  const { data: student } = useQuery({
    ...getStudentOptions({
      path: { student_id: studentId },
    }),
    enabled: !!studentId,
  });

  const updateStudentStatus = useMutation({
    ...updateStudentStatusMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getStudentQueryKey({
          path: { student_id: studentId },
        }),
      });
      navigate({ to: "/admin/registration/students" });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const onStatusChange = (newStatus: Status) => {
    updateStudentStatus.mutate({
      body: { status: newStatus, studentIds: [studentId] },
    });
  };

  if (!student)
    return null;

  const contentNav = [
    { name: "Overview", icon: Info },
    { name: "Lessons", icon: BookOpen },
    { name: "Notes", icon: FileText },
  ];

  return (
    <Card className="border-none">
      <CardContent className="flex h-screen">
        {/* Minimal sidebar */}
        <nav>
          <div className="flex flex-col items-center space-x-4 m-6">
            <Avatar className="w-24 h-24 mb-4">
              <AvatarImage src="/placeholder.svg" />
              <AvatarFallback>
                {getInitials(student.firstName, student.fatherName)}
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="flex flex-col items-center gap-2">
                <span>
                  {student.firstName}
                  {" "}
                  {student.fatherName}
                </span>
                {/* <StudentApplicationStatusBadge status={student.status} /> */}
                <p className="text-sm text-gray-500">
                  Grade
                  {" "}
                  {student.grade.grade}
                </p>
              </div>
            </div>
          </div>
          {contentNav.map(item => (
            <button
              key={item.name}
              className="flex items-center w-full gap-3 px-3 py-2 rounded-md hover:bg-gray-100"
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </button>
          ))}

          <div className="mt-5 flex justify-between gap-2">
            <StudentStatusActions
              currentStatus={student.status}
              onStatusChange={onStatusChange}
            />
          </div>
        </nav>
        <div className="flex flex-col flex-1 gap-4 ml-4 overflow-y-auto p-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Personal Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Full Name
                  </p>
                  <p className="font-medium">
                    {student.firstName}
                    {" "}
                    {student.fatherName}
                  </p>
                </div>
                {student.grandFatherName && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      Grandfather's Name
                    </p>
                    <p>{student.grandFatherName}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Date of Birth
                  </p>
                  <p>
                    {formatDate(student.dateOfBirth)}
                    {" "}
                    (
                    {calculateAge(student.dateOfBirth)}
                    {" "}
                    years old)
                  </p>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Gender
                  </p>
                  <p className="capitalize">{student.gender}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Nationality
                  </p>
                  <p>{student.nationality ? student.nationality : "N/A"}</p>
                </div>
                {student.bloodType && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      Blood Type
                    </p>
                    <Badge variant="outline" className="bg-red-50 text-red-700">
                      {student.bloodType}
                    </Badge>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Home className="h-5 w-5" />
                Family Contact Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="font-medium text-blue-600">Primary Parents</h4>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Father</p>
                    <p>{student.fatherName}</p>
                    <p className="text-sm text-gray-600">
                      {student.fatherPhone}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Mother's Phone
                    </p>
                    <p>{student.motherPhone}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Parent Email
                    </p>
                    <p>{student.parentEmail}</p>
                  </div>
                </div>
                <div className="space-y-3">
                  <h4 className="font-medium text-orange-600">
                    Additional Contacts
                  </h4>
                  {student.guardianName
                    ? (
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Guardian
                          </p>
                          <p>{student.guardianName}</p>
                          {student.guardianRelation && (
                            <p className="text-sm text-gray-600">
                              Relationship: (
                              {student.guardianRelation}
                              )
                            </p>
                          )}
                          {student.guardianPhone && (
                            <p className="text-sm text-gray-600">
                              {student.guardianPhone}
                            </p>
                          )}
                        </div>
                      )
                    : (
                        <p className="text-sm text-gray-500">
                          No guardian specified
                        </p>
                      )}
                  {student.emergencyContactName
                    ? (
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Emergency Contact
                          </p>
                          <p>{student.emergencyContactName}</p>
                          {student.emergencyContactPhone && (
                            <p className="text-sm text-gray-600">
                              {student.emergencyContactPhone}
                            </p>
                          )}
                        </div>
                      )
                    : (
                        <p className="text-sm text-gray-500">
                          No emergency contact specified
                        </p>
                      )}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="h-5 w-5" />
                Address Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Home Address
                </p>
                <p>{student.address}</p>
                <p>
                  {student.city}
                  ,
                  {student.state}
                  {" "}
                  {student.postalCode}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                  <Phone className="h-4 w-4" />
                  Parent Contact
                </p>
                <p>
                  Father:
                  {student.fatherPhone}
                </p>
                <p>
                  Mother:
                  {student.motherPhone}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                  <Mail className="h-4 w-4" />
                  Email
                </p>
                <p>{student.parentEmail}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <GraduationCap className="h-5 w-5" />
                Academic Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">Grade Level</p>
                <Badge className="bg-blue-100 text-blue-800">
                  Grade
                  {" "}
                  {student.grade.grade}
                </Badge>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Academic Year
                </p>
                <p>{student.grade.year.name || "N/A"}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Transfer Student
                </p>
                {student.isTransfer
                  ? (
                      <Badge
                        variant="outline"
                        className="bg-orange-100 text-orange-800"
                      >
                        Yes
                      </Badge>
                    )
                  : (
                      <Badge
                        variant="outline"
                        className="bg-green-100 text-green-800"
                      >
                        No
                      </Badge>
                    )}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Previous School
                </p>
                <p>{student.previousSchool || "N/A"}</p>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <Bus className="h-4 w-4 text-gray-500" />
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Transportation
                    </p>
                    <p className="capitalize">
                      {student.transportation || "N/A"}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Sibling Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Has Siblings
                </p>
                {student.siblingInSchool
                  ? (
                      <Badge
                        variant="outline"
                        className="bg-orange-100 text-orange-800"
                      >
                        Yes
                      </Badge>
                    )
                  : (
                      <Badge
                        variant="outline"
                        className="bg-green-100 text-green-800"
                      >
                        No
                      </Badge>
                    )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart className="h-5 w-5" />
                Medical Information & Special Needs
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium text-gray-500">
                  Medical Conditions:
                </p>
                {student.hasMedicalCondition
                  ? (
                      <Badge
                        variant="destructive"
                        className="flex items-center gap-1"
                      >
                        <AlertTriangle className="h-3 w-3" />
                        Yes
                      </Badge>
                    )
                  : (
                      <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                        <CheckCircle className="h-3 w-3" />
                        No
                      </Badge>
                    )}
              </div>
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium text-gray-500">
                  Disabilities:
                </p>
                {student.hasDisability
                  ? (
                      <Badge
                        variant="destructive"
                        className="flex items-center gap-1"
                      >
                        <AlertTriangle className="h-3 w-3" />
                        Yes
                      </Badge>
                    )
                  : (
                      <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                        <CheckCircle className="h-3 w-3" />
                        No
                      </Badge>
                    )}
              </div>
              {student.medicalDetails && (
                <div className="p-4 bg-red-50 rounded-lg">
                  <p className="text-sm font-medium text-red-800 mb-2">
                    Medical Condition Details:
                  </p>
                  <p className="text-sm text-red-700">
                    {student.medicalDetails}
                  </p>
                </div>
              )}
              {student.disabilityDetails && (
                <div className="p-4 bg-orange-50 rounded-lg">
                  <p className="text-sm font-medium text-orange-800 mb-2">
                    Disability Details:
                  </p>
                  <p className="text-sm text-orange-700">
                    {student.disabilityDetails}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  );
}

type StudentStatusActionsProps = {
  currentStatus: Status;
  onStatusChange: (newStatus: Status) => void;
};

const statusTransitions: Record<Status, Status[]> = {
  pending: ["active", "rejected"],
  rejected: ["pending"],
  active: ["inactive", "suspended", "graduated", "withdrawn"],
  inactive: ["active", "withdrawn"],
  graduated: [],
  suspended: ["active", "withdrawn"],
  withdrawn: ["pending"],
};

const statusMeta: Record<
  Status,
  { label: string; icon: React.ElementType; className?: string | undefined }
> = {
  pending: {
    label: "Pending",
    icon: Clock,
    className:
      "bg-yellow-100 text-yellow-800 border-yellow-200 hover:bg-yellow-500",
  },
  rejected: {
    label: "Reject",
    icon: XCircle,
    className: "bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-500",
  },
  active: {
    label: "Activate",
    icon: CheckCircle,
    className: "bg-green-100 hover:bg-green-500",
  },
  inactive: {
    label: "Deactivate",
    icon: Pause,
    className: "bg-red-100 hover:bg-red-500",
  },
  graduated: {
    label: "Graduate",
    icon: GraduationCap,
    className: "bg-green-100 hover:bg-green-500",
  },
  suspended: {
    label: "Suspend",
    icon: Ban,
    className: "bg-red-100 hover:bg-red-500",
  },
  withdrawn: {
    label: "Withdraw",
    icon: LogOut,
    className: "bg-red-100 hover:bg-red-500",
  },
};

export function StudentStatusActions({
  currentStatus,
  onStatusChange,
}: StudentStatusActionsProps) {
  const nextStatuses = statusTransitions[currentStatus] || [];

  if (nextStatuses.length === 0) {
    return (
      <p className="text-sm text-gray-500">No further actions available</p>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
      {nextStatuses.map((status) => {
        const { label, icon: Icon, className } = statusMeta[status];
        return (
          <Button
            key={status}
            variant="outline"
            size="sm"
            onClick={() => onStatusChange(status)}
            className={`flex items-center gap-2 ${className}`}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Button>
        );
      })}
    </div>
  );
}
