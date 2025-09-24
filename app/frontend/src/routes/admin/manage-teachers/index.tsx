import {
  assignTeacherMutation,
  getSectionsOptions,
  getSubjectSetupByIdOptions,
  getSubjectsOptions,
  getTeachersOptions,
} from "@/client/@tanstack/react-query.gen";
import { AssignTeacher, TeacherBasicInfo } from "@/client/types.gen";
import { zAssignTeacher } from "@/client/zod.gen";
import { ApiState } from "@/components/api-state";
import { teacherBasicInfoColumns } from "@/components/data-table/manage-teachers/columns";
import { ManageTeacherTable } from "@/components/data-table/manage-teachers/manage-teachers-table";
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
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { SelectItem } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, Plus, Users } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  FormProvider,
  SubmitHandler,
  useForm,
  UseFormReturn,
} from "react-hook-form";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/manage-teachers/")({
  component: RouteComponent,
  loader: async () => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getTeachersOptions({
          query: { q: "" },
        }),
      );
    }
  },
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();
  const [formDialogOpen, setFormDialogOpen] = useState(false);

  const getTeacherQueryConfig = () => ({
    query: { q: "" },
  });

  const { data: teachers } = useQuery({
    ...getTeachersOptions(getTeacherQueryConfig()),
    enabled: !!yearId,
  });

  const [defaultValues] = useState<AssignTeacher>({
    teacherId: "",
    yearId: yearId!,
    subjectId: "",
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

  const mutation = useMutation({
    ...assignTeacherMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries(
        getTeachersOptions(getTeacherQueryConfig()),
      );
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

  const handleView = (employeeId: string) => {
    navigate({ to: "/admin/employees/$employeeId", params: { employeeId } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Teacher Management
                </CardTitle>
                <CardDescription>
                  Review and manage all teacher Management in one place
                </CardDescription>
              </div>
              <AlertDialog
                open={formDialogOpen}
                onOpenChange={setFormDialogOpen}
              >
                <AlertDialogTrigger asChild>
                  <Button variant="default">
                    <Plus className="h-4 w-4 mr-2" />
                    New Assignment
                  </Button>
                </AlertDialogTrigger>

                <FormDialog
                  assignTeacherForm={assignTeacherForm}
                  teachers={teachers || []}
                  submitAssignTeacher={submitAssignTeacher}
                  isAssignTeacherPending={mutation.isPending}
                />
              </AlertDialog>
            </div>
          </CardHeader>
          <CardContent>
            <ManageTeacherTable
              columns={teacherBasicInfoColumns(handleView, teachers || [])}
              data={teachers || []}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function FormDialog({
  assignTeacherForm,
  teachers,
  submitAssignTeacher,
  isAssignTeacherPending,
}: {
  assignTeacherForm: UseFormReturn<AssignTeacher>;
  teachers: TeacherBasicInfo[];
  submitAssignTeacher: (data: AssignTeacher) => void;
  isAssignTeacherPending: boolean;
}) {
  const yearId = store.getState().year.id;
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

  const selectedGrade = useMemo(() => {
    return subject?.grades.find((grade) => grade.id === watchForm.grade.id);
  }, [subject, watchForm.grade.id]);

  const defaultSubject = useMemo(() => {
    if (!watchForm.teacherId) return undefined;
    return teachers.find((teacher) => teacher.id === watchForm.teacherId)
      ?.subject.id;
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

  console.log(watchForm);
  return (
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
                {teacher.fullName} - {teacher.subject.name}
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
                    watchForm.grade.sections.find((s) => s.id === section.id) ||
                    section
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
              disabled={!isDirty || isAssignTeacherPending}
              type="submit"
              onClick={handleSave}
              className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed w-32"
            >
              {isAssignTeacherPending && (
                <Loader className="animate-spin mr-2 h-4 w-4" />
              )}
              Save Changes
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </FormProvider>
    </AlertDialogContent>
  );
}
