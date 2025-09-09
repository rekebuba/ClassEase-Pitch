import {
  getGradesOptions,
  getStreamsOptions,
  getSubjectSetupByIdOptions,
  patchSubjectSetupMutation,
} from "@/client/@tanstack/react-query.gen";
import {
  GradeSchema,
  SubjectSetupSchema,
  UpdateSubjectSetup,
} from "@/client/types.gen";
import { zSubjectSetupSchema, zUpdateSubjectSetup } from "@/client/zod.gen";
import { ApiState } from "@/components/api-state";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { getDirtyValues } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ArrowLeft, GraduationCap, Loader } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/subjects/$subjectId/")({
  loader: async ({ params: { subjectId } }) => {
    const yearId = store.getState().year.id;
    await queryClient.ensureQueryData(
      getSubjectSetupByIdOptions({
        path: { subject_id: subjectId },
      }),
    );
    if (yearId) {
      await queryClient.ensureQueryData(
        getGradesOptions({
          query: { yearId },
        }),
      );
    }
  },
  component: RouteComponent,
});

export default function RouteComponent() {
  const subjectId = Route.useParams().subjectId!;
  const yearId = store.getState().year.id;
  const navigate = useNavigate();

  const {
    data: subject,
    isSuccess: isSubjectSuccess,
    isLoading: isSubjectLoading,
    error: isSubjectError,
  } = useQuery(
    getSubjectSetupByIdOptions({
      path: { subject_id: subjectId },
    }),
  );

  const {
    data: grades,
    isLoading: isGradesLoading,
    error: isGradesError,
  } = useQuery({
    ...getGradesOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const { data: streams } = useQuery({
    ...getStreamsOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const [defaultValues] = useState<SubjectSetupSchema>({
    id: crypto.randomUUID(),
    yearId: yearId || "",
    name: "",
    code: "",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    grades: [],
    streams: [],
  });

  const form = useForm<SubjectSetupSchema>({
    resolver: zodResolver(zSubjectSetupSchema),
    defaultValues,
  });
  const {
    formState: { dirtyFields, isDirty },
    reset,
    setError,
    handleSubmit,
  } = form;

  useEffect(() => {
    if (isSubjectSuccess && subject) {
      reset(subject);
    }
  }, [isSubjectSuccess, subject, reset]);

  const handleCancel = useCallback(() => {
    navigate({
      to: "/admin/subjects",
      search: { yearId: yearId! },
    });
  }, [yearId, navigate]);

  const mutation = useMutation({
    ...patchSubjectSetupMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      handleCancel();
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof SubjectSetupSchema, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error(
          "Failed to Update Subject Setup. Please Check Your inputs.",
          {
            style: { color: "red" },
          },
        );
      }
    },
  });

  const onValid: SubmitHandler<SubjectSetupSchema> = (data) => {
    const dirtyValues = getDirtyValues(dirtyFields, data);
    const result = zUpdateSubjectSetup.safeParse(dirtyValues);

    if (result.success) {
      const safeDirtyValues: UpdateSubjectSetup = result.data;
      // Use safely typed values
      mutation.mutate({
        path: { subject_id: subjectId },
        body: safeDirtyValues,
      });
    } else {
      toast.error("Failed to update Subject. Please Check Your Input.");
    }
  };

  // Form submission
  const handleSave = handleSubmit(onValid);

  if (!subject) return <div>Subject not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <ApiState isLoading={isSubjectLoading} error={isSubjectError?.message}>
          <div className="flex items-center gap-4">
            <Button variant="outline" size="sm" onClick={handleCancel}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div>
              <div className="flex gap-2 items-center">
                <GraduationCap className="text-blue-600" />
                <h1 className="text-2xl font-bold">{subject.name}</h1>
              </div>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-sm text-gray-600">
                  <div className="text-xs text-gray-500">
                    Last updated: {formatDate(subject.updatedAt)}
                  </div>
                </span>
              </div>
            </div>
          </div>
        </ApiState>
      </div>

      <FormProvider {...form}>
        <Card className="space-y-">
          <CardContent className="space-y-6 pt-4 border-t">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <InputWithLabel<SubjectSetupSchema>
                  fieldTitle="Subject Name *"
                  nameInSchema={`name`}
                  placeholder="e.g., Mathematics"
                />
              </div>
              <div>
                <InputWithLabel<SubjectSetupSchema>
                  fieldTitle="Subject Code *"
                  nameInSchema={`code`}
                  placeholder="e.g., MATH"
                />
              </div>
            </div>
            <div>
              <Label htmlFor="description">Description (Optional)</Label>
              <Textarea
                id="description"
                placeholder="Brief description of the subject..."
                rows={3}
              />
            </div>
            <div>
              <div className="pb-3">
                <Label className="text-lg font-semibold text-gray-900">
                  Taught in Grades
                </Label>
                <p className="text-sm text-gray-600 mt-1">
                  Select grades and their streams for this subject
                </p>
              </div>
              <Card className="shadow-sm">
                <CardContent className="p-6">
                  {/* Empty State */}
                  {subject.grades.length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                      <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>
                        No grades added yet. Add your first grade in the 'Grades
                        & Streams' Tab
                      </p>
                    </div>
                  )}
                  <ApiState
                    isLoading={isGradesLoading}
                    error={isGradesError?.message}
                  >
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {grades?.map((grade) => (
                        <GradesCheckbox
                          key={grade.id}
                          grade={grade}
                          streams={streams || []}
                          subjectGrades={subject.grades}
                        />
                      ))}
                    </div>
                  </ApiState>
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>
        {/* Action Buttons */}
        <CardFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
          <div className="ml-auto flex gap-3">
            <Button variant="outline" onClick={handleCancel}>
              Cancel
            </Button>
            <Button
              disabled={!isDirty || mutation.isPending}
              type="submit"
              onClick={handleSave}
              className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
            >
              {mutation.isPending && <Loader className="animate-spin" />}
              Save Changes
            </Button>
          </div>
        </CardFooter>
      </FormProvider>
    </div>
  );
}

function GradesCheckbox({
  grade,
  streams,
  subjectGrades,
}: {
  grade: GradeSchema;
  streams: SubjectSetupSchema["streams"];
  subjectGrades: SubjectSetupSchema["grades"];
}) {
  const streamsByGrade = useMemo(() => {
    return streams.filter((s) => s.gradeId === grade.id);
  }, [streams, grade.id]);

  return (
    <div
      key={grade.id}
      className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
    >
      {!grade.hasStream ? (
        <div className="flex flex-col space-x-4 space-y-4">
          <CheckboxWithLabel<
            SubjectSetupSchema,
            SubjectSetupSchema["grades"][number]
          >
            fieldTitle={`Grade ${grade.grade}`}
            nameInSchema="grades"
            value={subjectGrades.find((g) => g.id === grade.id) || grade}
            className="h-5 w-5 text-primary"
          />
          <Label className="text-sm font-medium">
            <p className="text-xs text-gray-400 italic">No Stream assigned</p>
          </Label>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <label>{`Grade ${grade.grade}`}</label>
          </div>

          <div className="ml-8 space-y-2">
            {streamsByGrade.map((stream) => (
              <div key={stream.id} className="flex items-center space-x-3">
                <CheckboxWithLabel<
                  SubjectSetupSchema,
                  SubjectSetupSchema["streams"][number]
                >
                  fieldTitle={`Grade ${grade.grade} (${stream.name})`}
                  nameInSchema="streams"
                  value={streams.find((s) => s.id === stream.id) || stream}
                  className="h-4 w-4 text-primary"
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
