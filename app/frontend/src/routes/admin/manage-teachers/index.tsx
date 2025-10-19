import {
  assignTeacherMutation,
  getAcademicTermsOptions,
  getSectionsOptions,
  getSubjectSetupByIdOptions,
  getSubjectsOptions,
  getTeachersOptions,
} from "@/client/@tanstack/react-query.gen";
import { AssignTeacher, TeacherBasicInfo } from "@/client/types.gen";
import { zAssignTeacher } from "@/client/zod.gen";
import { ApiState } from "@/components/api-state";
import EmployeeApplicationStatusBadge from "@/components/enum-badge/employee-application-status-badge";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { getInitials } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import {
  BookOpen,
  Edit,
  Eye,
  Filter,
  GraduationCap,
  Loader,
  Mail,
  MoreHorizontal,
  Plus,
  Search,
  UserPlus,
  Users,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/manage-teachers/")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      const academicTerms = await queryClient.ensureQueryData(
        getAcademicTermsOptions({
          query: { yearId: yearId },
        }),
      );

      await queryClient.ensureQueryData(
        getTeachersOptions({
          query: {
            q: "",
            yearId: yearId,
            academicTermId: academicTerms[0]?.id,
          },
        }),
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [selectedAcademicTerm, setSelectedAcademicTerm] = useState<string>("");

  const {
    data: academicTerms,
    isLoading: isLoadingAcademicTerms,
    error: isAcademicTermsError,
  } = useQuery({
    ...getAcademicTermsOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  useEffect(() => {
    if (academicTerms && academicTerms.length > 0) {
      const firstTerm = academicTerms[0];
      setSelectedAcademicTerm(firstTerm.id);
    }
  }, [academicTerms]);

  const getTeacherQueryConfig = () => ({
    query: { q: "", yearId: yearId!, academicTermId: selectedAcademicTerm },
  });

  const { data: teachers } = useQuery({
    ...getTeachersOptions(getTeacherQueryConfig()),
    enabled: !!yearId && !!selectedAcademicTerm,
  });

  // const handleView = (employeeId: string) => {
  //   navigate({ to: "/admin/employees/$employeeId", params: { employeeId } });
  // };

  const teacherGrades = (length: number) => {
    switch (length) {
      case 0:
        return `grid-cols-1`;
      case 1:
        return `grid-cols-1`;
      case 2:
        return `grid-cols-2`;
      case 3:
        return `grid-cols-3`;
      default:
        return `grid-cols-4`;
    }
  };

  return (
    <Card className="">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="font-semibold flex items-center gap-2">
              <Users className="h-5 w-5" />
              Teacher Management
            </CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <FormDialog
              teachers={teachers || []}
              trigger={
                <Button
                  size="sm"
                  className="flex-1 bg-primary hover:bg-primary/90"
                >
                  <UserPlus className="w-3.5 h-3.5 mr-1.5" />
                  Assign
                </Button>
              }
            />
          </div>
        </div>

        <div className="flex items-center gap-4 mt-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search teachers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-input border-border"
            />
          </div>

          <ApiState
            isLoading={isLoadingAcademicTerms}
            error={isAcademicTermsError?.message}
          >
            <Select
              defaultValue={selectedAcademicTerm}
              onValueChange={setSelectedAcademicTerm}
            >
              <SelectTrigger className="w-[280px]">
                <SelectValue placeholder="Academic Term" />
              </SelectTrigger>
              <SelectContent>
                {academicTerms?.map((term) => (
                  <SelectItem key={term.id} value={term.id}>
                    Term {term.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </ApiState>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="outline"
                className="border-border bg-transparent"
              >
                <Filter className="w-4 h-4 mr-2" />
                Status: {statusFilter === "all" ? "All" : statusFilter}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => setStatusFilter("all")}>
                All Status
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setStatusFilter("active")}>
                Active
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setStatusFilter("on_leave")}>
                On Leave
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setStatusFilter("inactive")}>
                Inactive
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {teachers?.map((teacher) => (
            <Card
              key={teacher.id}
              className="bg-muted/30 border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg"
            >
              <CardContent className="p-6">
                {/* Header with Avatar and Actions */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <Avatar className="w-14 h-14 ring-2 ring-primary/20">
                      <AvatarImage src={undefined} />
                      <AvatarFallback className="bg-primary/10 text-primary font-semibold text-lg">
                        {getInitials(teacher.firstName, teacher.fatherName)}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-semibold text-lg text-foreground">
                        {teacher.firstName} {teacher.fatherName}
                      </h3>
                      <div className="flex items-center gap-2 mt-1">
                        {EmployeeApplicationStatusBadge({
                          status: teacher.status,
                        })}
                      </div>
                    </div>
                  </div>

                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="w-8 h-8 -mt-1"
                      >
                        <MoreHorizontal className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link
                          to="/admin/employees/$employeeId"
                          params={{ employeeId: teacher.id }}
                          className="flex items-center"
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          View Profile
                        </Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <Edit className="w-4 h-4 mr-2" />
                        Edit Details
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>

                {/* Contact Information */}
                <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4 pb-4 border-b border-border">
                  <Mail className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">{teacher.email}</span>
                </div>

                {/* Main Subject */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="mb-4">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen className="w-4 h-4 text-primary" />
                      <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        Main Subject
                      </span>
                    </div>
                    <div className="font-semibold text-foreground text-base">
                      {teacher.mainSubject?.name}
                    </div>
                  </div>
                  {/* Secondary Subjects */}
                  {teacher.otherSubjects.length > 0 && (
                    <div className="mb-4">
                      <div className="flex items-center gap-2 mb-2">
                        <GraduationCap className="w-4 h-4 text-primary" />
                        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                          Additional Subjects
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        <Badge variant="secondary" className="text-xs">
                          {teacher.otherSubjects.length} Subjects
                        </Badge>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 mb-2">
                  <Users className="w-4 h-4 text-primary" />
                  <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                    Current Assignments
                  </span>
                  {teacher.grades.length > 4 && (
                    <Badge variant="outline" className="text-xs">
                      +{teacher.grades.length - 4} more
                    </Badge>
                  )}
                </div>
                <div
                  className={`grid gap-3 pt-4 border-t ${teacherGrades(teacher.grades.length)}`}
                >
                  {teacher.grades.length > 0 ? (
                    teacher.grades.slice(0, 4).map((grade) => (
                      <div className="text-center">
                        <div className="flex items-center justify-center gap-1 mb-1">
                          <GraduationCap className="w-3.5 h-3.5 text-muted-foreground" />
                        </div>
                        <div className="font-semibold text-foreground">
                          Grade {grade.grade}
                        </div>
                        <div className="flex items-center justify-center gap-1 text-xs text-muted-foreground">
                          {grade.subjects.map((subject) => (
                            <span key={subject.id}>{subject.code}</span>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center">No grades assigned</div>
                  )}
                </div>

                {/* Quick Actions */}
                <div className="flex gap-2 mt-4">
                  <Button
                    asChild
                    variant="outline"
                    size="sm"
                    className="flex-1 border-border bg-transparent"
                  >
                    <Link
                      to="/admin/employees/$employeeId"
                      params={{ employeeId: teacher.id }}
                    >
                      <Eye className="w-3.5 h-3.5 mr-1.5" />
                      View Profile
                    </Link>
                  </Button>
                  <FormDialog
                    teachers={teachers || []}
                    teacherId={teacher.id}
                    subjectId={teacher.mainSubject?.id}
                    trigger={
                      <Button
                        size="sm"
                        className="flex-1 bg-primary hover:bg-primary/90"
                      >
                        <Plus className="w-3.5 h-3.5 mr-1.5" />
                        Assign
                      </Button>
                    }
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function FormDialog({
  teachers,
  teacherId,
  subjectId,
  trigger,
}: {
  teachers: TeacherBasicInfo[];
  teacherId?: string;
  subjectId?: string;
  trigger?: React.ReactNode;
}) {
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const yearId = store.getState().year.id;

  const [defaultValues] = useState<AssignTeacher>({
    teacherId: teacherId || "",
    yearId: yearId!,
    subjectId: subjectId || "",
    grade: {
      id: "",
      streamId: "",
      sections: [],
    },
  });

  const assignTeacherForm = useForm<AssignTeacher>({
    resolver: zodResolver(zAssignTeacher),
    defaultValues,
  });

  const {
    formState: { isDirty },
    watch,
    setValue,
    handleSubmit,
  } = assignTeacherForm;
  const watchForm = watch();

  const getSubjectsQueryConfig = () => ({
    query: { yearId: yearId!, q: "" },
  });

  const {
    data: subjects,
    isLoading: isSubjectsLoading,
    error: isSubjectsError,
  } = useQuery(getSubjectsOptions(getSubjectsQueryConfig()));

  const {
    data: subject,
    isLoading: isSubjectLoading,
    error: isSubjectError,
  } = useQuery({
    ...getSubjectSetupByIdOptions({
      path: { subject_id: watchForm.subjectId },
    }),
    enabled: !!watchForm.subjectId,
  });

  const {
    data: sections,
    isLoading: isSectionsLoading,
    error: isSectionsError,
  } = useQuery({
    ...getSectionsOptions({
      query: { gradeId: watchForm.grade.id },
    }),
    enabled: !!watchForm.grade.id,
  });

  const mutation = useMutation({
    ...assignTeacherMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getTeachersOptions().queryKey,
      });
      assignTeacherForm.reset(defaultValues);
      setFormDialogOpen(false);
    },
    onError: (error) => {
      const detail = error.response?.data.detail;

      if (detail && Array.isArray(detail) && detail.length > 0) {
        const first = detail[0];
        if (first?.loc?.[1]) {
          assignTeacherForm.setError(first.loc[1] as keyof AssignTeacher, {
            type: "server",
            message: first.msg,
          });
        }
      } else if (detail && typeof detail === "string") {
        toast.error(detail || "Something went wrong. Please try again.");
      }
    },
  });

  const submitAssignTeacher: SubmitHandler<AssignTeacher> = (data) => {
    mutation.mutate({
      body: data,
    });
  };

  const selectedGrade = useMemo(() => {
    return subject?.grades.find((grade) => grade.id === watchForm.grade.id);
  }, [subject, watchForm.grade.id]);

  const defaultSubject = useMemo(() => {
    if (!watchForm.teacherId) return undefined;
    return teachers.find((teacher) => teacher.id === watchForm.teacherId)
      ?.mainSubject?.id;
  }, [teachers, watchForm.teacherId]);

  useEffect(() => {
    setValue("grade", { id: "", streamId: "", sections: [] });
  }, [watchForm.subjectId, setValue]);

  useEffect(() => {
    if (defaultSubject) {
      setValue("subjectId", defaultSubject);
    }
  }, [defaultSubject, setValue]);

  // Form submission
  const handleSave = handleSubmit(submitAssignTeacher);

  const joinId = (gradeId: string, streamId?: string) => {
    return streamId ? `${gradeId},${streamId}` : gradeId;
  };

  const getGradeObject = (joinedId: string): AssignTeacher["grade"] => {
    const [gradeId, streamId] = joinedId.split(",").map((id) => id.trim());

    return {
      id: gradeId,
      streamId: streamId || null,
      sections: [],
    };
  };

  const defaultTrigger = (
    <Button className="bg-primary hover:bg-primary/90">
      <Plus className="w-4 h-4 mr-2" />
      New Assignment
    </Button>
  );

  console.log(watchForm);
  return (
    <AlertDialog open={formDialogOpen} onOpenChange={setFormDialogOpen}>
      <AlertDialogTrigger asChild>
        {trigger || defaultTrigger}
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Create New Assignment</AlertDialogTitle>
          <AlertDialogDescription>
            Assign a teacher to a specific grade, section, and subject.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <Separator />
        <FormProvider {...assignTeacherForm}>
          <div className="space-y-6">
            <SelectWithLabel<AssignTeacher, string>
              fieldTitle="Teacher *"
              nameInSchema="teacherId"
            >
              {teachers.map((teacher) => (
                <SelectItem key={teacher.id} value={teacher.id}>
                  {teacher.fullName} - {teacher.mainSubject?.name}
                </SelectItem>
              ))}
            </SelectWithLabel>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SelectWithLabel<AssignTeacher, string>
                fieldTitle="Subject *"
                nameInSchema="subjectId"
              >
                <ApiState
                  isLoading={isSubjectsLoading}
                  error={isSubjectsError?.message}
                >
                  {subjects?.map((subject) => (
                    <SelectItem key={subject.id} value={subject.id}>
                      {subject.name}
                    </SelectItem>
                  ))}
                </ApiState>
              </SelectWithLabel>
              <SelectWithLabel<AssignTeacher, AssignTeacher["grade"]>
                fieldTitle="Grade *"
                nameInSchema="grade"
                getObjects={(joinedId) => getGradeObject(joinedId)}
              >
                <ApiState
                  isLoading={isSubjectLoading}
                  error={isSubjectError?.message}
                >
                  {subject?.grades.map((grade) => (
                    <>
                      {!grade.hasStream ? (
                        <SelectItem key={grade.id} value={joinId(grade.id)}>
                          Grade {grade.grade}
                        </SelectItem>
                      ) : (
                        <div>
                          {subject.streams
                            .filter((s) => s.gradeId === grade.id)
                            .map((stream) => (
                              <SelectItem
                                key={stream.id}
                                value={joinId(grade.id, stream.id)}
                              >
                                Grade {grade.grade} - {stream.name}
                              </SelectItem>
                            ))}
                        </div>
                      )}
                    </>
                  ))}
                </ApiState>
              </SelectWithLabel>
            </div>
            <div className="grid grid-row-3 md:grid-cols-1 gap-4">
              <ApiState
                isLoading={isSectionsLoading}
                error={isSectionsError?.message}
              >
                {sections && (
                  <div className="">
                    <Label className="text-sm">
                      Grade {selectedGrade?.grade || ""} Sections *
                    </Label>
                  </div>
                )}
                {sections?.map((section) => (
                  <CheckboxWithLabel<
                    AssignTeacher,
                    AssignTeacher["grade"]["sections"][number]
                  >
                    nameInSchema={`grade.sections`}
                    fieldTitle={`Section ${section.section}`}
                    value={
                      watchForm.grade.sections.find(
                        (s) => s.id === section.id,
                      ) || section
                    }
                  />
                ))}
              </ApiState>
            </div>
          </div>

          {/* Action Buttons */}
          <AlertDialogFooter className="mt-5">
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction asChild>
              <Button
                disabled={!isDirty || mutation.isPending}
                type="submit"
                onClick={handleSave}
                className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed w-32"
              >
                {mutation.isPending && (
                  <Loader className="animate-spin mr-2 h-4 w-4" />
                )}
                Save Changes
              </Button>
            </AlertDialogAction>
          </AlertDialogFooter>
        </FormProvider>
      </AlertDialogContent>
    </AlertDialog>
  );
}
