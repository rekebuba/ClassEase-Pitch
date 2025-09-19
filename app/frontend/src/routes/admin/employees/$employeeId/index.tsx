import {
  getEmployeeOptions,
  getEmployeeQueryKey,
  updateEmployeeStatusMutation,
} from "@/client/@tanstack/react-query.gen";
import { EmployeeApplicationStatusEnum as Status } from "@/client/types.gen";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { calculateAge, getInitials } from "@/utils/utils";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  Ban,
  BookOpen,
  Briefcase,
  CheckCircle,
  Clock,
  FileText,
  Home,
  Info,
  LogOut,
  Mail,
  Pause,
  Phone,
  User,
  Users,
  XCircle,
} from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/employees/$employeeId/")({
  component: RouteComponent,
  loader: async ({ params }) => {
    await queryClient.ensureQueryData(
      getEmployeeOptions({
        path: { employee_id: params.employeeId },
      }),
    );
  },
});

interface EmployeeStatusActionsProps {
  currentStatus: Status;
  onStatusChange: (newStatus: Status) => void;
}

const statusTransitions: Record<Status, Status[]> = {
  pending: ["active", "approved", "rejected"],
  rejected: ["pending", "interview-scheduled"],
  active: ["inactive", "withdrawn"],
  inactive: ["active", "withdrawn"],
  "interview-scheduled": ["approved", "rejected"],
  approved: ["active", "withdrawn"],
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
  "interview-scheduled": {
    label: "interview-scheduled",
    icon: Ban,
    className: "bg-red-100 hover:bg-red-500",
  },
  approved: {
    label: "approved",
    icon: LogOut,
    className: "bg-red-100 hover:bg-red-500",
  },
  withdrawn: {
    label: "Withdraw",
    icon: LogOut,
    className: "bg-red-100 hover:bg-red-500",
  },
};

export function EmployeeStatusActions({
  currentStatus,
  onStatusChange,
}: EmployeeStatusActionsProps) {
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

function RouteComponent() {
  const employeeId = Route.useParams().employeeId;
  const navigate = useNavigate();

  const { data: employee } = useQuery({
    ...getEmployeeOptions({
      path: { employee_id: employeeId },
    }),
    enabled: !!employeeId,
  });

  const updateEmployeeStatus = useMutation({
    ...updateEmployeeStatusMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getEmployeeQueryKey({
          path: { employee_id: employeeId },
        }),
      });
      navigate({ to: "/admin/registration/employees" });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const onStatusChange = (newStatus: Status) => {
    updateEmployeeStatus.mutate({
      body: { status: newStatus, employeeIds: [employeeId] },
    });
  };

  if (!employee) return null;

  const contentNav = [
    { name: "Overview", icon: Info },
    { name: "Schedule", icon: BookOpen },
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
                {getInitials(employee.firstName, employee.fatherName)}
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="flex flex-col items-center gap-2">
                <span>
                  {employee.firstName} {employee.fatherName}
                </span>
                {/* <EmployeeApplicationStatusBadge status={employee.status} /> */}
                <p className="text-sm text-gray-500 capitalize">
                  {employee.position}
                </p>
              </div>
            </div>
          </div>
          {contentNav.map((item) => (
            <button
              key={item.name}
              className="flex items-center w-full gap-3 px-3 py-2 rounded-md hover:bg-gray-100"
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </button>
          ))}

          <div className="mt-5 flex justify-between gap-2">
            <EmployeeStatusActions
              currentStatus={employee.status}
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
                    {employee.firstName} {employee.fatherName}
                  </p>
                </div>
                {employee.grandFatherName && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      Grandfather's Name
                    </p>
                    <p>{employee.grandFatherName}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Date of Birth
                  </p>
                  <p>
                    {formatDate(employee.dateOfBirth)} (
                    {calculateAge(employee.dateOfBirth)} years old)
                  </p>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Gender
                  </p>
                  <p className="capitalize">{employee.gender}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Nationality
                  </p>
                  <p>{employee.nationality ? employee.nationality : "N/A"}</p>
                </div>
                {employee.maritalStatus && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      Marital Status
                    </p>
                    <p className="capitalize">{employee.maritalStatus}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Home className="h-5 w-5" />
                Contact Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-500">Address</p>
                  <p>{employee.address}</p>
                  <p>
                    {employee.city}, {employee.state}, {employee.country}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                    <Phone className="h-4 w-4" />
                    Primary Phone
                  </p>
                  <p>{employee.primaryPhone}</p>
                </div>
                {employee.secondaryPhone && (
                  <div>
                    <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                      <Phone className="h-4 w-4" />
                      Secondary Phone
                    </p>
                    <p>{employee.secondaryPhone}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                    <Mail className="h-4 w-4" />
                    Email
                  </p>
                  <p>{employee.personalEmail}</p>
                </div>
              </div>
              <div className="space-y-4">
                <h4 className="font-medium text-red-600">Emergency Contact</h4>
                {employee.emergencyContactName ? (
                  <div>
                    <p className="text-sm font-medium text-gray-500">Name</p>
                    <p>{employee.emergencyContactName}</p>
                    {employee.emergencyContactRelation && (
                      <p className="text-sm text-gray-600">
                        Relationship: ({employee.emergencyContactRelation})
                      </p>
                    )}
                    {employee.emergencyContactPhone && (
                      <p className="text-sm text-gray-600">
                        {employee.emergencyContactPhone}
                      </p>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">
                    No emergency contact specified
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Professional & Educational Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">Position</p>
                <Badge className="bg-blue-100 text-blue-800 capitalize">
                  {employee.position}
                </Badge>
              </div>
              {employee.subjects && (
                <div>
                  <p className="text-sm font-medium text-gray-500">
                    Teaching Subject
                  </p>
                  <p>
                    {employee.subjects
                      .map((subject) => subject.name)
                      .join(", ")}
                  </p>
                </div>
              )}
              <div>
                <p className="text-sm font-medium text-gray-500">Experience</p>
                <p>{employee.yearsOfExperience} Years</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Highest Education
                </p>
                <p>{employee.highestEducation}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">University</p>
                <p>{employee.university}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Graduation Year
                </p>
                <p>{employee.graduationYear}</p>
              </div>
              {employee.gpa && (
                <div>
                  <p className="text-sm font-medium text-gray-500">GPA</p>
                  <p>{employee.gpa}</p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Reference Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <h4 className="font-medium text-blue-600">Reference</h4>
                {employee.reference1Name ? (
                  <>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Name</p>
                      <p>{employee.reference1Name}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">
                        Organization
                      </p>
                      <p>{employee.reference1Organization}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Phone</p>
                      <p>{employee.reference1Phone}</p>
                    </div>
                    {employee.reference1Email && (
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Email
                        </p>
                        <p>{employee.reference1Email}</p>
                      </div>
                    )}
                  </>
                ) : (
                  <p className="text-sm text-gray-500">
                    No reference provided.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Documents & Agreements
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">Resume/CV</p>
                {employee.resume ? (
                  <Button variant="link" asChild>
                    <a
                      href={employee.resume as string}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View Resume
                    </a>
                  </Button>
                ) : (
                  <p>Not provided</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  );
}
