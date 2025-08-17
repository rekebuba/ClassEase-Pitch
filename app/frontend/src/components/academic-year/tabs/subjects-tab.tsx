import { SubjectSetupCard } from "@/components/academic-year/form-setup";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { YearSetupType } from "@/lib/api-response-type";
import { BookOpen, Edit, Plus, Search, Trash } from "lucide-react";
import { useMemo, useState } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";
import { toast } from "sonner";

type Subject = YearSetupType["subjects"][number];

export default function SubjectsTab({
  onDirty,
}: {
  onDirty: (dirty: boolean) => void;
}) {
  const {
    formState: { isDirty },
    control,
    watch,
  } = useFormContext<YearSetupType>();

  const [searchTerm, setSearchTerm] = useState("");
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [formMode, setFormMode] = useState<"create" | "edit">("create");
  const [formIndex, setFormIndex] = useState<number>(0);

  const { fields: subjectFields, prepend: prependSubject } = useFieldArray({
    control: control,
    name: "subjects",
    keyName: "rhfId", // Prevents overriding `id`
  });

  const watchSubjects = watch("subjects");

  const filteredSubjects = watchSubjects.filter((subject) => {
    const matchesSearch =
      subject.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      subject.code.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  const handleCreateSubject = () => {
    prependSubject({
      id: crypto.randomUUID(),
      name: "",
      code: "",
      grades: [],
      streams: [],
    }); // Add empty subject
    setFormMode("create");
    setFormIndex(0); // Always edit the first subject in the list
    setFormDialogOpen(true);
  };

  // Report dirty state
  onDirty(isDirty);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="pb-4">
          <CardTitle className="text-xl font-semibold">
            Subject Management
          </CardTitle>
          <p className="text-sm text-gray-500">
            Configure subjects for your academic year
          </p>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Search & Add */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search subjects..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Button
              onClick={() => handleCreateSubject()}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Subject
            </Button>
          </div>

          {/* Empty State */}
          {filteredSubjects.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>
                {subjectFields.length > 0 && searchTerm !== ""
                  ? `No subjects match your search ${searchTerm}.`
                  : "No subjects added yet. Add your first subject above."}
              </p>
            </div>
          )}

          {/* Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSubjects.map((subject, index) => (
              <SubjectGradesCard
                key={subject.id}
                subject={subject}
                index={index}
                setFormMode={setFormMode}
                setFormIndex={setFormIndex}
                setFormDialogOpen={setFormDialogOpen}
              />
            ))}
          </div>
        </CardContent>
      </Card>

      <SubjectSetupCard
        open={formDialogOpen}
        onOpenChange={setFormDialogOpen}
        formIndex={formIndex}
        mode={formMode}
      />
    </div>
  );
}

interface SubjectGradesCardProps {
  subject: Subject;
  index: number;
  setFormMode: (mode: "create" | "edit") => void;
  setFormIndex: (index: number) => void;
  setFormDialogOpen: (open: boolean) => void;
}

const SubjectGradesCard = ({
  subject,
  index,
  setFormMode,
  setFormIndex,
  setFormDialogOpen,
}: SubjectGradesCardProps) => {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const { control, watch } = useFormContext<YearSetupType>();
  // Grades field array
  const { remove: removeSubject } = useFieldArray({
    control,
    name: "subjects",
    keyName: "rhfId",
  });
  const watchGrades = watch("grades");

  const filteredGrades = useMemo(() => {
    return watchGrades.filter((grade) =>
      grade.subjects.some((s) => s.id === subject.id),
    );
  }, [watchGrades, subject.id]);

  return (
    <Card
      key={subject.id}
      className="flex flex-col justify-between min-h-[220px] p-4 border border-gray-200 hover:shadow-lg transition-shadow"
    >
      {/* Title */}
      <div>
        <CardTitle className="flex items-center gap-2 mb-2 text-md">
          <BookOpen className="text-blue-600 shrink-0" />
          <span className="truncate">{subject.name}</span>
          <Badge className="text-[13px] px-2" variant="outline">
            {subject.code}
          </Badge>
        </CardTitle>

        {/* Grades */}
        <div className="mt-3">
          <h4 className="font-medium mb-3 text-sm text-gray-600">Taught In</h4>
          {subject.grades.length > 0 || subject.streams.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {filteredGrades.map((grade) => (
                <div key={`grade-${grade.id}`}>
                  {grade.hasStream ? (
                    grade.streams
                      .filter((stream) =>
                        stream.subjects.some((s) => s.id === subject.id),
                      )
                      .map((stream) => (
                        <Badge
                          key={`stream-${stream.id}`}
                          variant="default"
                          className="text-xs"
                        >
                          Grade {grade.grade} ({stream.name})
                        </Badge>
                      ))
                  ) : (
                    <Badge
                      key={`grade-only-${grade.id}`}
                      variant="secondary"
                      className="text-xs"
                    >
                      Grade {grade.grade}
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-gray-400 italic">No grades assigned</p>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2 mt-4">
        <Separator />
        <div className="flex gap-2 mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setDeleteDialogOpen(true)}
            className="flex-1 border-gray-300 hover:bg-red-50"
          >
            <Trash className="h-4 w-4 mr-1" />
            Remove
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setFormDialogOpen(true);
              setFormMode("edit");
              setFormIndex(index);
            }}
            className="flex-1 border-gray-300 hover:bg-blue-50"
          >
            <Edit className="h-4 w-4 mr-1" />
            Edit
          </Button>
        </div>
      </div>

      <DeleteConfirmationDialog
        open={deleteDialogOpen}
        onStay={() => setDeleteDialogOpen(false)}
        onDiscard={() => {
          removeSubject(index);
          setDeleteDialogOpen(false);
          toast.success("Subject removed successfully");
        }}
      />
    </Card>
  );
};

function DeleteConfirmationDialog({
  open,
  onStay,
  onDiscard,
}: {
  open: boolean;
  onStay: () => void;
  onDiscard: () => void;
}) {
  return (
    <AlertDialog open={open} onOpenChange={onStay}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you Absolutely Sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This will Delete the subject and all its associated data.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={onStay}>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={onDiscard}
            className="bg-red-500 hover:bg-red-400"
          >
            <Trash className="h-4 w-4 mr-1" />
            Remove
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
