"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  User,
  MapPin,
  GraduationCap,
  Heart,
  Users,
  FileText,
  Phone,
  Mail,
  Home,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Eye,
  Bus,
  Utensils,
  Activity,
} from "lucide-react";
import type { StudentApplication } from "@/lib/api-validation";
import { StudentStatusBadge } from "@/components";

interface StudentDetailDialogProps {
  student: StudentApplication | null;
  isOpen: boolean;
  onClose: () => void;
  onStatusChange: (
    studentId: string,
    newStatus: StudentApplication["status"],
  ) => void;
}

export default function StudentDetailDialog({
  student,
  isOpen,
  onClose,
  onStatusChange,
}: StudentDetailDialogProps) {
  const [isUpdating, setIsUpdating] = useState(false);

  if (!student) return null;

  const handleStatusChange = async (
    newStatus: StudentApplication["status"],
  ) => {
    setIsUpdating(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    onStatusChange(student.id, newStatus);
    setIsUpdating(false);
  };

  const getInitials = (firstName: string, fatherName: string) => {
    return `${firstName.charAt(0)}${fatherName.charAt(0)}`.toUpperCase();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
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

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="fixed top-10 right-[10%] max-w-6xl max-h-[90vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <Avatar className="h-10 w-10">
              <AvatarImage src={student.studentPhoto || "/placeholder.svg"} />
              <AvatarFallback>
                {getInitials(student.firstName, student.fatherName)}
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="flex items-center gap-2">
                <span>
                  {student.firstName} {student.fatherName}
                </span>
                <StudentStatusBadge status={student.status} />
              </div>
              <p className="text-sm text-gray-500">
                {student.grade} • {student.academicYear}
              </p>
            </div>
          </DialogTitle>
        </DialogHeader>

        <ScrollArea className="max-h-[calc(90vh-120px)]">
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  <Button
                    size="sm"
                    variant={
                      student.status === "under-review" ? "default" : "outline"
                    }
                    onClick={() => handleStatusChange("under-review")}
                    disabled={isUpdating}
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    Review
                  </Button>
                  <Button
                    size="sm"
                    variant={
                      student.status === "documents-required"
                        ? "default"
                        : "outline"
                    }
                    onClick={() => handleStatusChange("documents-required")}
                    disabled={isUpdating}
                  >
                    <FileText className="h-4 w-4 mr-1" />
                    Request Documents
                  </Button>
                  <Button
                    size="sm"
                    variant={
                      student.status === "approved" ? "default" : "outline"
                    }
                    onClick={() => handleStatusChange("approved")}
                    disabled={isUpdating}
                    className="bg-green-600 hover:bg-green-700 text-white"
                  >
                    <CheckCircle className="h-4 w-4 mr-1" />
                    Approve
                  </Button>
                  <Button
                    size="sm"
                    variant={
                      student.status === "enrolled" ? "default" : "outline"
                    }
                    onClick={() => handleStatusChange("enrolled")}
                    disabled={isUpdating}
                    className="bg-purple-600 hover:bg-purple-700 text-white"
                  >
                    <GraduationCap className="h-4 w-4 mr-1" />
                    Enroll
                  </Button>
                  <Button
                    size="sm"
                    variant={
                      student.status === "rejected" ? "destructive" : "outline"
                    }
                    onClick={() => handleStatusChange("rejected")}
                    disabled={isUpdating}
                  >
                    <XCircle className="h-4 w-4 mr-1" />
                    Reject
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Tabs defaultValue="personal" className="w-full">
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="personal">Personal</TabsTrigger>
                <TabsTrigger value="academic">Academic</TabsTrigger>
                <TabsTrigger value="contact">Contact</TabsTrigger>
                <TabsTrigger value="medical">Medical</TabsTrigger>
                <TabsTrigger value="additional">Additional</TabsTrigger>
              </TabsList>

              <TabsContent value="personal" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <User className="h-5 w-5" />
                        Personal Information
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Full Name
                        </p>
                        <p>
                          {student.firstName} {student.fatherName}
                        </p>
                      </div>
                      <div></div>
                      {student.grandFatherName && (
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Grandfather's Name
                          </p>
                          <p>{student.grandFatherName}</p>
                        </div>
                      )}
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Date of Birth
                        </p>
                        <p>
                          {formatDate(student.dateOfBirth)} (
                          {calculateAge(student.dateOfBirth)} years old)
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Gender
                        </p>
                        <p className="capitalize">{student.gender}</p>
                      </div>
                      {student.nationality && (
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Nationality
                          </p>
                          <p>{student.nationality}</p>
                        </div>
                      )}
                      {student.bloodType && (
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Blood Type
                          </p>
                          <Badge variant="outline">{student.bloodType}</Badge>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <MapPin className="h-5 w-5" />
                        Address Information
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Home Address
                        </p>
                        <p>{student.address}</p>
                        <p>
                          {student.city}, {student.state} {student.postalCode}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                          <Phone className="h-4 w-4" />
                          Parent Contact
                        </p>
                        <p>Father: {student.fatherPhone}</p>
                        <p>Mother: {student.motherPhone}</p>
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
                </div>

                {(student.guardianName || student.emergencyContactName) && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Users className="h-5 w-5" />
                        Guardian & Emergency Contact
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {student.guardianName && (
                          <div>
                            <p className="text-sm font-medium text-gray-500">
                              Guardian
                            </p>
                            <p>{student.guardianName}</p>
                            {student.guardianRelation && (
                              <p className="text-sm text-gray-600">
                                Relationship: {student.guardianRelation}
                              </p>
                            )}
                            {student.guardianPhone && (
                              <p className="text-sm text-gray-600">
                                {student.guardianPhone}
                              </p>
                            )}
                          </div>
                        )}
                        {student.emergencyContactName && (
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
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="academic" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <GraduationCap className="h-5 w-5" />
                      Academic Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Grade Level
                        </p>
                        <Badge className="bg-blue-100 text-blue-800">
                          {student.grade}
                        </Badge>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Academic Year
                        </p>
                        <p>{student.academicYear}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-500">
                          Transfer Student
                        </p>
                        {student.isTransfer ? (
                          <Badge
                            variant="outline"
                            className="bg-orange-100 text-orange-800"
                          >
                            Yes
                          </Badge>
                        ) : (
                          <Badge
                            variant="outline"
                            className="bg-green-100 text-green-800"
                          >
                            No
                          </Badge>
                        )}
                      </div>
                    </div>

                    {student.isTransfer && student.previousSchool && (
                      <div className="p-4 bg-orange-50 rounded-lg">
                        <p className="text-sm font-medium text-orange-800 mb-2">
                          Transfer Information
                        </p>
                        <p className="text-sm">
                          <strong>Previous School:</strong>{" "}
                          {student.previousSchool}
                        </p>
                        {student.previousGrades && (
                          <p className="text-sm mt-1">
                            <strong>Previous Performance:</strong>{" "}
                            {student.previousGrades}
                          </p>
                        )}
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {student.transportation && (
                        <div className="flex items-center gap-2">
                          <Bus className="h-4 w-4 text-gray-500" />
                          <div>
                            <p className="text-sm font-medium text-gray-500">
                              Transportation
                            </p>
                            <p className="capitalize">
                              {student.transportation.replace("-", " ")}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>

                {student.siblingInSchool && student.siblingDetails && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Users className="h-5 w-5" />
                        Sibling Information
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="whitespace-pre-wrap">
                        {student.siblingDetails}
                      </p>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="contact" className="space-y-4">
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
                        <h4 className="font-medium text-blue-600">
                          Primary Parents
                        </h4>
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Father
                          </p>
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
                        {student.guardianName ? (
                          <div>
                            <p className="text-sm font-medium text-gray-500">
                              Guardian
                            </p>
                            <p>{student.guardianName}</p>
                            {student.guardianRelation && (
                              <p className="text-sm text-gray-600">
                                ({student.guardianRelation})
                              </p>
                            )}
                            {student.guardianPhone && (
                              <p className="text-sm text-gray-600">
                                {student.guardianPhone}
                              </p>
                            )}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">
                            No guardian specified
                          </p>
                        )}

                        {student.emergencyContactName ? (
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
                        ) : (
                          <p className="text-sm text-gray-500">
                            No emergency contact specified
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="medical" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Heart className="h-5 w-5" />
                      Medical Information & Special Needs
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-medium text-gray-500">
                          Medical Conditions:
                        </p>
                        {student.hasMedicalCondition ? (
                          <Badge
                            variant="destructive"
                            className="flex items-center gap-1"
                          >
                            <AlertTriangle className="h-3 w-3" />
                            Yes
                          </Badge>
                        ) : (
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
                        {student.hasDisability ? (
                          <Badge
                            variant="destructive"
                            className="flex items-center gap-1"
                          >
                            <AlertTriangle className="h-3 w-3" />
                            Yes
                          </Badge>
                        ) : (
                          <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                            <CheckCircle className="h-3 w-3" />
                            No
                          </Badge>
                        )}
                      </div>
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

                    {!student.hasMedicalCondition && !student.hasDisability && (
                      <div className="p-4 bg-green-50 rounded-lg text-center">
                        <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                        <p className="text-sm text-green-800">
                          No medical concerns or special needs reported
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="additional" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Registration Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                      <p>
                        <strong>Student:</strong> {student.firstName}{" "}
                        {student.fatherName}
                      </p>
                      <p>
                        <strong>Grade:</strong> {student.grade}
                      </p>
                      <p>
                        <strong>Academic Year:</strong> {student.academicYear}
                      </p>
                      <p>
                        <strong>Father:</strong> {student.fatherName}
                      </p>
                      <p>
                        <strong>Contact:</strong> {student.fatherPhone}
                      </p>
                      <p>
                        <strong>Registration Date:</strong>{" "}
                        {formatDate(student.registrationDate)}
                      </p>
                      {student.isTransfer && (
                        <p>
                          <strong>Transfer Student:</strong> Yes (from{" "}
                          {student.previousSchool})
                        </p>
                      )}
                      {student.hasMedicalCondition && (
                        <p className="text-red-600">
                          <strong>⚠️ Medical Condition:</strong> Requires
                          attention
                        </p>
                      )}
                      {student.hasDisability && (
                        <p className="text-orange-600">
                          <strong>⚠️ Disability:</strong> Special support needed
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
