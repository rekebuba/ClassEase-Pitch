import { getEmployeeOptions } from "@/client/@tanstack/react-query.gen";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { calculateAge } from "@/utils/utils";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import {
  Briefcase,
  FileText,
  Home,
  Mail,
  Phone,
  User,
  Users,
} from "lucide-react";

export const Route = createFileRoute("/admin/employees/$employeeId/profile/")({
  component: RouteComponent,
  loader: async ({ params }) => {
    await queryClient.ensureQueryData(
      getEmployeeOptions({
        path: { employee_id: params.employeeId },
      }),
    );
  },
});

function RouteComponent() {
  const employeeId = Route.useParams().employeeId;

  const { data: employee } = useQuery({
    ...getEmployeeOptions({
      path: { employee_id: employeeId },
    }),
    enabled: !!employeeId,
  });

  if (!employee) return null;

  return (
    <Card className="border-none space-y-6">
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
          <div>
            <p className="text-sm font-medium text-gray-500">Major Subject</p>
            <p>{employee.subject?.name}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">
              Additional Subjects
            </p>
            <p>
              {employee.subjects.map((subject) => subject.name).join(", ") ||
                "N/A"}
            </p>
          </div>
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
            <p className="text-sm font-medium text-gray-500">Graduation Year</p>
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
                    <p className="text-sm font-medium text-gray-500">Email</p>
                    <p>{employee.reference1Email}</p>
                  </div>
                )}
              </>
            ) : (
              <p className="text-sm text-gray-500">No reference provided.</p>
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
    </Card>
  );
}
