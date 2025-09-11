import {
  getGradesOptions,
  getGradesSetupByIdOptions,
  getSubjectsOptions,
  patchGradeSetupMutation,
} from "@/client/@tanstack/react-query.gen";
import {
  GradeSetupSchema,
  SubjectSchema,
  UpdateGradeSetup,
} from "@/client/types.gen";
import {
  zGradeEnum,
  zGradeLevelEnum,
  zGradeSetupSchema,
  zUpdateGradeSetup,
} from "@/client/zod.gen";
import AdvanceTooltip from "@/components/advance-tooltip";
import { ApiState } from "@/components/api-state";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { SwitchWithLabel } from "@/components/inputs/switch-labeled";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SelectItem } from "@/components/ui/select";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { getDirtyValues } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  ArrowLeft,
  BookOpen,
  GraduationCap,
  Layers,
  Loader,
  PencilIcon,
  Plus,
  Trash,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  FormProvider,
  SubmitHandler,
  useFieldArray,
  useForm,
  useFormContext,
} from "react-hook-form";
import { toast } from "sonner";

export const Route = createFileRoute("/admin/grades/$gradeId/")({
  loader: async ({ params: { gradeId } }) => {
    const yearId = store.getState().year.id;
    await queryClient.ensureQueryData(
      getGradesSetupByIdOptions({
        path: { grade_id: gradeId },
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

function RouteComponent() {
  const gradeId = Route.useParams().gradeId!;
  const yearId = store.getState().year.id;
  const navigate = useNavigate();
  const {
    data: grade,
    isSuccess: isGradeSuccess,
    isLoading: isGradeLoading,
    error: isGradeError,
  } = useQuery(
    getGradesSetupByIdOptions({
      path: { grade_id: gradeId },
    }),
  );

  const { data: grades } = useQuery({
    ...getGradesOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const {
    data: subjects,
    isLoading: isSubjectsLoading,
    error: isSubjectsError,
  } = useQuery({
    ...getSubjectsOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const availableGrades = useMemo(() => {
    // Get all currently selected grades from parent
    const otherSelectedGrades =
      grades?.filter((g) => g.grade !== grade?.grade).map((g) => g.grade) || [];

    // Filter out already selected grades
    return zGradeEnum.options.filter(
      (gradeOption) => !otherSelectedGrades.includes(gradeOption),
    );
  }, [grade?.grade, grades]);

  const [defaultValues] = useState<GradeSetupSchema>({
    id: crypto.randomUUID(),
    yearId: crypto.randomUUID(),
    grade: "1",
    level: "primary",
    hasStream: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    subjects: [],
    sections: [],
    streams: [],
  });

  const form = useForm<GradeSetupSchema>({
    resolver: zodResolver(zGradeSetupSchema),
    defaultValues,
  });
  const {
    formState: { dirtyFields, isDirty },
    setValue,
    reset,
    watch,
    handleSubmit,
    setError,
  } = form;

  useEffect(() => {
    if (isGradeSuccess && grade) {
      reset(grade);
    }
  }, [isGradeSuccess, grade, reset]);

  const watchForm = watch();
  const watchSection = watchForm.sections;

  const mutation = useMutation({
    ...patchGradeSetupMutation(),
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
          setError(field as keyof GradeSetupSchema, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Update Grade Setup.");
      }
    },
  });

  const handleCancel = useCallback(() => {
    navigate({
      to: "/admin/grades",
    });
  }, [navigate]);

  if (!grade) return <div>Grade not found</div>;

  const onValid: SubmitHandler<GradeSetupSchema> = (data) => {
    if (!watchForm.hasStream) {
      setValue(`streams`, [], { shouldDirty: true });
    }

    const dirtyValues = getDirtyValues(dirtyFields, data);
    const result = zUpdateGradeSetup.safeParse(dirtyValues);

    if (result.success) {
      const safeDirtyValues: UpdateGradeSetup = result.data;
      // Use safely typed values
      mutation.mutate({
        path: { grade_id: gradeId },
        body: safeDirtyValues,
      });
    } else {
      toast.error("Failed to update grade. Please check your input.");
    }
  };

  const handleSave = handleSubmit(onValid);

  const generateSections = (maxSections: number) =>
    Array.from({ length: maxSections }, (_, i) => String.fromCharCode(65 + i));

  const getSectionObjects = (
    countStr: string,
  ): GradeSetupSchema["sections"] => {
    const sectionCount = parseInt(countStr, 10);

    if (isNaN(sectionCount) || sectionCount < 1 || sectionCount > 26) {
      console.error(
        "Invalid section count. Must be a number between 1 and 26.",
      );
      return [];
    }

    return Array.from({ length: sectionCount }, (_, i) => ({
      id: watchSection[i]?.id || crypto.randomUUID(),
      gradeId: watchForm.id,
      section: watchSection[i]?.section || String.fromCharCode(65 + i),
    }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <ApiState isLoading={isGradeLoading} error={isGradeError?.message}>
          <div className="flex items-center gap-4">
            <Button variant="outline" size="sm" onClick={handleCancel}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div>
              <div className="flex gap-2 items-center">
                <GraduationCap className="text-blue-600" />
                <h1 className="text-2xl font-bold">Grade {grade?.grade}</h1>
              </div>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-sm text-gray-600">
                  <div className="text-xs text-gray-500">
                    Last updated: {formatDate(grade.updatedAt)}
                  </div>
                </span>
              </div>
            </div>
          </div>
        </ApiState>
      </div>

      <FormProvider {...form}>
        <Card className="space-y-4">
          <CardContent className="space-y-6 pt-4 border-t">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Grade Name */}
              <SelectWithLabel<GradeSetupSchema, string>
                fieldTitle="Grade Level *"
                nameInSchema={`grade`}
              >
                {availableGrades.map((grade) => (
                  <SelectItem key={grade} value={grade}>
                    Grade {grade}
                  </SelectItem>
                ))}
              </SelectWithLabel>

              {/* Grade Level */}
              <SelectWithLabel<GradeSetupSchema, string>
                fieldTitle="Grade Level *"
                nameInSchema={`level`}
              >
                {zGradeLevelEnum.options.map((level) => (
                  <SelectItem key={level} value={level}>
                    {level}
                  </SelectItem>
                ))}
              </SelectWithLabel>
            </div>

            {/* Sections */}
            <SelectWithLabel<GradeSetupSchema, GradeSetupSchema["sections"]>
              fieldTitle="Sections *"
              nameInSchema={`sections`}
              getObjects={(index) => getSectionObjects(index)}
            >
              {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                <SelectItem key={num} value={num.toString()}>
                  {num} Section{num > 1 ? "s" : ""} (
                  {generateSections(num).join(", ")})
                </SelectItem>
              ))}
            </SelectWithLabel>
            <div className="flex gap-1 mt-2">
              {grade?.sections.map((section) => (
                <Badge key={section.id} variant="outline">
                  Section {section.section}
                </Badge>
              ))}
            </div>
            {/* Streams Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <Label>Has Streams/Tracks</Label>
                <p className="text-sm text-gray-500">
                  Enable different academic tracks for this grade
                </p>
              </div>
              <SwitchWithLabel fieldTitle="" nameInSchema={`hasStream`} />
            </div>

            {/* Streams Management */}
            {watchForm.hasStream && <StreamsManagement subjects={subjects} />}

            {/* Grade Subjects (for non-stream grades) */}
            {!watchForm.hasStream && (
              <div>
                <Label>Grade Subjects</Label>
                <p className="text-sm text-gray-500 mb-3">
                  Select subjects for this grade
                </p>

                <Card className="shadow-sm">
                  <CardContent className="p-6">
                    {/* Empty State */}
                    {subjects?.length === 0 && (
                      <div className="text-center py-12 text-gray-500">
                        <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                        <p>
                          No subjects added yet. Add your first subject in the
                          'Subjects' Tab
                        </p>
                      </div>
                    )}

                    <ApiState
                      isLoading={isSubjectsLoading}
                      error={isSubjectsError?.message}
                    >
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {subjects?.map((subject) => (
                          <div
                            key={subject.id}
                            className="flex items-center space-x-2"
                          >
                            <CheckboxWithLabel<
                              GradeSetupSchema,
                              GradeSetupSchema["subjects"][number]
                            >
                              fieldTitle={subject.name}
                              nameInSchema={`subjects`}
                              value={
                                grade.subjects.find(
                                  (s) => s.id === subject.id,
                                ) || subject
                              }
                              className="w-4 h-4"
                            />
                          </div>
                        ))}
                      </div>
                    </ApiState>
                  </CardContent>
                </Card>
              </div>
            )}
          </CardContent>
        </Card>
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

interface StreamsManagementProps {
  subjects: SubjectSchema[] | undefined;
}

function StreamsManagement({ subjects }: StreamsManagementProps) {
  const { control, watch } = useFormContext<GradeSetupSchema>();
  const [newStreamName, setNewStreamName] = useState("");

  const [isOpen, setIsOpen] = useState(false);

  const { prepend: prependStream, remove: removeStream } = useFieldArray({
    control,
    name: `streams`,
    keyName: "rhfId",
  });

  const watchGrade = watch(); // watch only this grade

  const handleSave = async () => {
    if (newStreamName === "") return;

    prependStream({
      id: crypto.randomUUID(),
      gradeId: watchGrade.id,
      name: newStreamName,
      subjects: [],
    });

    toast.success("New Stream Added To the List");
    setIsOpen(false);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Layers className="h-4 w-4" />
        <Label>Academic Streams</Label>
      </div>

      <div className="flex flex-wrap gap-2">
        {/* Add Custom Stream */}
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm" className="text-sm">
              <Plus className="h-4 w-4 mr-1" />
              Add Custom Stream Name
            </Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-[425px]">
            <div className="relative">
              <DialogHeader>
                <DialogTitle>Custom Stream Name</DialogTitle>
                <DialogDescription>
                  Enter a name for the custom stream you want to create.
                </DialogDescription>
              </DialogHeader>
            </div>

            <div>
              <Input
                value={newStreamName}
                onChange={(e) => setNewStreamName(e.target.value)}
                placeholder="e.g, Natural Stream, Social Stream..."
              />
            </div>

            <DialogFooter>
              <Button
                className="mt-0"
                variant="outline"
                onClick={() => setIsOpen(false)}
              >
                Cancel
              </Button>

              <Button
                disabled={watchGrade.streams[0]?.name?.length < 1}
                type="submit"
                onClick={handleSave}
                className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
              >
                Add Stream
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stream List */}
      <div className="space-y-3">
        {watchGrade.streams.map((stream, streamIndex) => (
          <Card key={stream.id} className="p-4">
            <div className="flex items-start justify-between mb-1">
              <div className="group flex items-center gap-2 cursor-pointer">
                <h4 className="font-medium text-gray-800">{stream.name}</h4>
                <AdvanceTooltip
                  tooltip="Rename Stream"
                  size="sm"
                  // onClick={() => renameStream(streamIndex)}
                  className="cursor-pointer bg-transparent h-8 w-8 rounded-full font-bold"
                >
                  <PencilIcon className="h-4 w-4" />
                </AdvanceTooltip>
              </div>
              <AdvanceTooltip
                tooltip="Delete"
                size="sm"
                onClick={() => removeStream(streamIndex)}
                className="ml-2 h-10 w-10 rounded-full"
              >
                <Trash className="h-4 w-4" />
              </AdvanceTooltip>
            </div>

            <div className="mb-4">
              <Label className="text-sm">Stream Subjects</Label>
            </div>

            {/* Empty State */}
            {subjects?.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>
                  No subjects added yet. Add your first subject in the
                  'Subjects' Tab
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {subjects?.map((subject) => (
                <div key={subject.id} className="flex items-center space-x-2">
                  <CheckboxWithLabel<
                    GradeSetupSchema,
                    GradeSetupSchema["subjects"][number]
                  >
                    fieldTitle={subject.name}
                    nameInSchema={`streams.${streamIndex}.subjects`}
                    value={
                      watchGrade.streams[streamIndex].subjects.find(
                        (s) => s.name === subject.name,
                      ) || subject
                    }
                    className="w-4 h-4"
                  />
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
