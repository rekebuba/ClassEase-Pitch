import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { SwitchWithLabel } from "@/components/inputs/switch-labeled";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
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
import { YearSetupType } from "@/lib/api-response-type";
import { YearSetupSchema } from "@/lib/api-response-validation";
import { GradeEnum, GradeLevelEnum } from "@/lib/enums";
import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, X, Layers, GraduationCap, BookOpen } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  FormProvider,
  SubmitErrorHandler,
  SubmitHandler,
  useFieldArray,
  useForm,
  useFormContext,
  UseFormReturn,
} from "react-hook-form";
import { toast } from "sonner";

type Grade = YearSetupType["grades"][number];
type Subject = YearSetupType["grades"][number]["subjects"][number];
type Stream = YearSetupType["grades"][number]["streams"][number];
type Section = YearSetupType["grades"][number]["sections"];

interface GradeSetupCardProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  formIndex: number;
  mode: "create" | "edit";
}

export default function GradeSetupCard({
  open,
  onOpenChange,
  mode,
  formIndex,
}: GradeSetupCardProps) {
  const {
    control,
    watch: parentWatch,
    setValue,
    getValues,
  } = useFormContext<YearSetupType>();

  const { remove: removeGrade } = useFieldArray({
    control,
    name: "grades",
  });
  const gradeForm = getValues(`grades.${formIndex}`);

  // Isolated sub-form for modal
  const subForm = useForm<Grade>({
    resolver: zodResolver(YearSetupSchema.shape.grades.element), // validate single subject
    defaultValues: gradeForm,
  });
  const {
    formState: { isDirty, dirtyFields },
    handleSubmit,
    watch: subWatch,
    reset,
  } = subForm;

  // Sync between parent and sub-form
  useEffect(() => {
    if (open) {
      const parentData = getValues(`grades.${formIndex}`);
      reset(parentData);
    }
  }, [open, formIndex, getValues, reset]);

  const watchParentForm = parentWatch();
  const watchSubForm = subWatch();

  const generateSections = (maxSections: number) =>
    Array.from({ length: maxSections }, (_, i) => String.fromCharCode(65 + i));

  const getSectionObjects = (countStr: string) => {
    const sectionCount = parseInt(countStr, 10);

    if (isNaN(sectionCount) || sectionCount < 1 || sectionCount > 26) {
      console.error(
        "Invalid section count. Must be a number between 1 and 26.",
      );
      return [];
    }

    const watchSection = watchParentForm.grades[formIndex].sections;
    return Array.from({ length: sectionCount }, (_, i) => ({
      id: watchSection[i]?.id || crypto.randomUUID(),
      gradeId: watchSection[i]?.gradeId || "",
      section: watchSection[i]?.section || String.fromCharCode(65 + i),
    }));
  };

  const availableGrades = useMemo(() => {
    // Get all currently selected grades from parent form
    const otherSelectedGrades =
      watchParentForm.grades
        ?.filter((g) => g.grade !== watchSubForm.grade)
        .map((g) => g.grade) || [];

    // Filter out already selected grades
    return GradeEnum.options.filter(
      (gradeOption) => !otherSelectedGrades.includes(gradeOption),
    );
  }, [watchParentForm.grades, watchSubForm]);

  // Utility: dedupe and sort by id
  // A process of eliminating redundant copies of data.
  const dedupeAndSort = <T extends { id: string }>(arr: T[]) =>
    arr
      .filter((v, i, a) => a.findIndex((x) => x.id === v.id) === i)
      .sort((a, b) => a.id.localeCompare(b.id));

  const syncSubjectsFromGrades = useCallback(() => {
    const grade = watchSubForm || {};
    const subjects = watchParentForm.subjects || [];

    if (!grade.id) return; // No valid grade to sync

    const gradeEntry = {
      id: grade.id,
      yearId: grade.yearId,
      grade: grade.grade,
      level: grade.level,
      hasStream: grade.hasStream,
    };

    const updatedSubjects = subjects.map((subject) => {
      const hasThisGrade = grade.subjects?.some((s) => s.id === subject.id);

      // Grade-level sync
      const updatedGrades = !grade.hasStream
        ? dedupeAndSort(
            hasThisGrade
              ? [...(subject.grades || []), gradeEntry]
              : (subject.grades || []).filter((g) => g.id !== grade.id),
          )
        : subject.grades || [];

      // Stream-level sync
      const updatedStreams = (() => {
        const withoutGradeStreams = (subject.streams || []).filter(
          (st) => st.gradeId !== grade.id,
        );
        const streamsFromGrade = (grade.streams || [])
          .filter((stream) => stream.subjects?.some((s) => s.id === subject.id))
          .map((stream) => ({
            id: stream.id,
            name: stream.name,
            gradeId: grade.id,
          }));
        return dedupeAndSort([...withoutGradeStreams, ...streamsFromGrade]);
      })();

      return { ...subject, grades: updatedGrades, streams: updatedStreams };
    });

    setValue("subjects", updatedSubjects, {
      shouldValidate: false,
      shouldDirty: true,
    });
  }, [watchSubForm, watchParentForm?.subjects, setValue]);

  const mergeStreamSubjects = useCallback(() => {
    const grade = watchSubForm || {};
    const mergedSubjects = [
      ...new Map(
        grade.streams
          .flatMap((stream) => stream.subjects) // gather all subjects
          .map((subject) => [subject.id, subject]), // map by id
      ).values(),
    ] as Subject[];

    setValue(`grades.${formIndex}.subjects`, mergedSubjects, {
      shouldValidate: false,
      shouldDirty: true,
    });
  }, [watchSubForm, watchParentForm?.subjects, setValue]);

  const onError: SubmitErrorHandler<Grade> = (error) => {
    toast.warning("There is missing information", {
      style: { color: "brown" },
      description: "Please Fill all required Fields marked with *",
    });
  };

  const onValid: SubmitHandler<Grade> = (data) => {
    setValue(`grades.${formIndex}`, data, { shouldDirty: true });
    if (dirtyFields.subjects || dirtyFields.streams || dirtyFields.hasStream) {
      syncSubjectsFromGrades();
      toast.success(
        mode === "create" ? "New Subject Added" : "Subject updated",
      );
    }
    if (!watchSubForm.hasStream) {
      setValue(`grades.${formIndex}.streams`, [], { shouldDirty: true });
    } else if (dirtyFields.streams) {
      mergeStreamSubjects();
    }
    onOpenChange(false);
    toast.success(mode === "create" ? "New Grade Added" : "Grade updated");
  };

  const handleSave = handleSubmit(onValid, onError);

  const handleCancel = () => {
    if (mode === "create") {
      removeGrade(formIndex);
    } else {
      reset(getValues(`grades.${formIndex}`));
    }
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={handleCancel}>
      <DialogContent className="max-w-5xl flex flex-col max-h-[90vh]">
        <DialogHeader className="flex items-center justify-between border-b pb-4 text-lg font-semibold">
          <div className="flex items-center gap-2">
            <GraduationCap className="text-blue-600" />
            <DialogTitle>Configure Grade</DialogTitle>
          </div>
          <DialogDescription>
            {watchSubForm?.grade ? "Configure" : "Create New"} grade level and
            academic tracks.
          </DialogDescription>
        </DialogHeader>
        <FormProvider {...subForm}>
          <div className="flex-grow overflow-y-auto space-y-4">
            <Card className="w-full transition-all duration-300">
              <CardContent className="space-y-6 pt-4 border-t">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Grade Name */}
                  <SelectWithLabel<Grade, string>
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
                  <SelectWithLabel<Grade, string>
                    fieldTitle="Grade Level *"
                    nameInSchema={`level`}
                  >
                    {GradeLevelEnum.options.map((level) => (
                      <SelectItem key={level} value={level}>
                        {level}
                      </SelectItem>
                    ))}
                  </SelectWithLabel>
                </div>

                {/* Sections */}
                <SelectWithLabel<Grade, Section>
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
                  {watchSubForm.sections.map((section) => (
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
                {watchSubForm.hasStream && (
                  <StreamsManagement
                    subjects={watchParentForm.subjects.map(
                      ({ id, name, code }) => ({ id, name, code }),
                    )}
                  />
                )}
                {/* Grade Subjects (for non-stream grades) */}
                {!watchSubForm.hasStream && (
                  <div>
                    <Label>Grade Subjects</Label>
                    <p className="text-sm text-gray-500 mb-3">
                      Select subjects for this grade
                    </p>

                    <Card className="shadow-sm">
                      <CardContent className="p-6">
                        {/* Empty State */}
                        {watchParentForm.subjects.length === 0 && (
                          <div className="text-center py-12 text-gray-500">
                            <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                            <p>
                              No subjects added yet. Add your first subject in
                              the 'Subjects' Tab
                            </p>
                          </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {watchParentForm.subjects.map(
                            (subject, subjectIndex) => (
                              <div
                                key={subject.id}
                                className="flex items-center space-x-2"
                              >
                                <CheckboxWithLabel<Grade, Subject>
                                  fieldTitle={subject.name}
                                  nameInSchema={`subjects`}
                                  value={
                                    watchSubForm.subjects.find(
                                      (s) => s.id === subject.id,
                                    ) || {
                                      id: subject.id,
                                      name: subject.name,
                                      code: subject.code,
                                    }
                                  }
                                  className="w-4 h-4"
                                />
                              </div>
                            ),
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}

                {/* Grade Summary */}
                <div className="bg-gray-50 p-3 rounded-lg">
                  <h3 className="font-medium mb-2">Configuration Summary</h3>
                  {/* <GradeSummary /> */}
                </div>
              </CardContent>
            </Card>
          </div>
          <DialogFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
            <div className="ml-auto flex gap-3">
              <Button variant="outline" onClick={handleCancel}>
                Cancel
              </Button>
              <Button
                disabled={!isDirty}
                type="submit"
                onClick={handleSave}
                className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
              >
                {mode === "create" ? "Create Grade" : "Save Changes"}
              </Button>
            </div>
          </DialogFooter>
        </FormProvider>
      </DialogContent>
    </Dialog>
  );
}

interface StreamsManagementProps {
  subjects: Subject[];
}

function StreamsManagement({ subjects }: StreamsManagementProps) {
  const { control, watch, trigger } = useFormContext<Grade>();
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
              <div>
                <h4 className="font-medium">{stream.name}</h4>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => removeStream(streamIndex)}
                className="ml-2"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            <div className="mb-4">
              <Label className="text-sm">Stream Subjects</Label>
            </div>

            {/* Empty State */}
            {subjects.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>
                  No subjects added yet. Add your first subject in the
                  'Subjects' Tab
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {subjects.map((subject) => (
                <div key={subject.id} className="flex items-center space-x-2">
                  <CheckboxWithLabel<Grade, Subject>
                    fieldTitle={subject.name}
                    nameInSchema={`streams.${streamIndex}.subjects`}
                    value={
                      watchGrade.streams[streamIndex].subjects.find(
                        (s) => s.name === subject.name,
                      ) || {
                        id: subject.id,
                        name: subject.name,
                        code: subject.code,
                      }
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
