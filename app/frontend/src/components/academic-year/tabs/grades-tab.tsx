import { YearSetupType } from "@/lib/api-response-type";
import { useFieldArray, useFormContext } from "react-hook-form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  BookOpen,
  ChevronDown,
  ChevronUp,
  Edit,
  GraduationCap,
  Plus,
  Search,
  Trash,
  Users,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useCallback, useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { GradeSetupCard } from "@/components/academic-year/form-setup";
import { GradeEnum } from "@/lib/enums";

type Grade = YearSetupType["grades"][number];
type Stream = YearSetupType["grades"][number]["streams"][number];

export default function GradesTab({
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

  // Grades field array
  const { fields: gradeFields, prepend: prependGrade } = useFieldArray({
    control,
    name: "grades",
    keyName: "rhfId",
  });

  const watchYear = watch();
  const watchGrades = watch("grades");

  const filteredGrades = watchGrades.filter((grade) =>
    grade.grade.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const handleCreateGrade = useCallback(() => {
    prependGrade({
      id: crypto.randomUUID(),
      yearId: watchYear.id,
      grade: "",
      level: "primary",
      hasStream: false,
      streams: [],
      sections: [],
      subjects: [],
    });
    setFormMode("create");
    setFormIndex(0);
    setFormDialogOpen(true);
  }, [prependGrade]);

  // Report dirty state
  onDirty(isDirty);

  return (
    <Card>
      <CardHeader className="pb-4">
        <CardTitle className="text-xl font-semibold">
          Grade Levels & Academic Streams
        </CardTitle>
        <p className="text-sm text-gray-500">
          Configure the grade levels and academic tracks for your school
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Search & Add */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search grades..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <Button
            onClick={() => handleCreateGrade()}
            disabled={GradeEnum.options.length <= gradeFields.length}
            className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Grade
          </Button>
        </div>

        {/* Empty State */}
        {filteredGrades.length === 0 && (
          <EmptyState
            hasGrades={gradeFields.length > 0}
            searchTerm={searchTerm}
          />
        )}

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredGrades.map((grade, index) => (
            <GradeSubjectsCard
              key={grade.id}
              grade={grade}
              index={index}
              setFormDialogOpen={setFormDialogOpen}
              setFormIndex={setFormIndex}
              setFormMode={setFormMode}
            />
          ))}
        </div>
      </CardContent>

      {filteredGrades.length > 0 && (
        <GradeSetupCard
          open={formDialogOpen}
          onOpenChange={setFormDialogOpen}
          formIndex={formIndex}
          mode={formMode}
        />
      )}
    </Card>
  );
}

interface GradeSubjectsCardProps {
  grade: Grade;
  index: number;
  setFormMode: (mode: "create" | "edit") => void;
  setFormIndex: (index: number) => void;
  setFormDialogOpen: (open: boolean) => void;
}

const GradeSubjectsCard = ({
  grade,
  index,
  setFormMode,
  setFormIndex,
  setFormDialogOpen,
}: GradeSubjectsCardProps) => {
  const { control, watch } = useFormContext<YearSetupType>();

  // Grades field array
  const { remove: removeGrade } = useFieldArray({
    control,
    name: "grades",
    keyName: "rhfId",
  });
  const watchSubjects = watch("subjects");

  const filteredSubjects = useMemo(() => {
    return watchSubjects.filter((subject) =>
      subject.grades.some((g) => g.id === grade.id),
    );
  }, [watchSubjects, grade.id]);

  return (
    <Card
      key={grade.id}
      className="flex flex-col justify-between min-h-[260px] p-4 border border-gray-200 hover:shadow-lg transition-shadow"
    >
      {/* Header */}
      <div>
        <CardTitle className="flex items-center gap-2 mb-3 text-md">
          <GraduationCap className="text-blue-600 shrink-0" />
          Grade {grade.grade}
          {grade.level && (
            <Badge className="text-[13px] px-2" variant="outline">
              {grade.level}
            </Badge>
          )}
        </CardTitle>

        {/* Info Stats */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="text-center p-2 bg-blue-50 rounded-lg">
            <GraduationCap className="h-4 w-4 text-blue-600 mx-auto mb-1" />
            <div className="text-sm font-semibold text-blue-900">
              {grade.sections.length}
            </div>
            <div className="text-xs text-blue-700">Sections</div>
          </div>

          <div className="text-center p-2 bg-purple-50 rounded-lg">
            <Users className="h-4 w-4 text-purple-600 mx-auto mb-1" />
            <div className="text-sm font-semibold text-purple-900">
              {grade.streams.length}
            </div>
            <div className="text-xs text-purple-700">Streams</div>
          </div>

          <div className="text-center p-2 bg-red-50 rounded-lg">
            <BookOpen className="h-4 w-4 text-red-600 mx-auto mb-1" />
            <div className="text-sm font-semibold text-red-900">
              {grade.hasStream
                ? new Set(
                    grade.streams
                      .flatMap((stream) => stream.subjects || [])
                      .map((subject) => subject.id),
                  ).size
                : grade.subjects.length}
            </div>
            <div className="text-xs text-red-700">Subjects</div>
          </div>
        </div>

        {/* Subject List */}
        <div className="mb-4">
          <h4 className="font-medium mb-3 text-sm text-gray-600">Subjects</h4>
          {grade.streams.length === 0 && grade.subjects.length === 0 ? (
            <p className="text-xs text-gray-400 italic">No subjects assigned</p>
          ) : (
            <>
              {grade.hasStream && grade.streams.length > 0 ? (
                <div className="mb-3 space-y-2">
                  {grade.streams.map((stream, streamIndex) => (
                    <CollapsibleStreamCard
                      key={streamIndex}
                      formIndex={index}
                      stream={stream}
                      streamIndex={streamIndex}
                    />
                  ))}
                </div>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {filteredSubjects.map((subject) => (
                    <Badge
                      key={subject.id}
                      variant="secondary"
                      className="text-xs"
                    >
                      {subject.name}
                    </Badge>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2">
        <Separator />
        <div className="flex gap-2 mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => removeGrade(index)}
            className="flex-1 border-gray-300 hover:bg-red-50"
          >
            <Trash className="h-4 w-4 mr-1" />
            Remove
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setFormMode("edit");
              setFormIndex(index);
              setFormDialogOpen(true);
            }}
            className="flex-1 border-gray-300 hover:bg-blue-50"
          >
            <Edit className="h-4 w-4 mr-1" />
            Edit
          </Button>
        </div>
      </div>
    </Card>
  );
};

interface CollapsibleStreamCardProps {
  stream: Stream;
  formIndex: number;
  streamIndex: number;
}

const CollapsibleStreamCard = ({
  stream,
  formIndex,
  streamIndex,
}: CollapsibleStreamCardProps) => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <Card className="p-2 bg-gray-50 hover:bg-gray-100 transition-colors border-l-4 border-l-purple-300 mb-3">
      <div
        className="flex items-center justify-between cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
        aria-label={`${isExpanded ? "Collapse" : "Expand"} ${stream.name} subjects`}
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Badge
            variant="outline"
            className="bg-purple-100 text-black-700 text-xs"
          >
            {stream.name}
          </Badge>
          <Badge
            variant="outline"
            className="bg-red-100 text-black-700 text-xs"
          >
            {stream.subjects?.length || 0} Subjects
          </Badge>
        </div>
        {isExpanded ? (
          <ChevronUp className="h-4 w-4 text-gray-500" />
        ) : (
          <ChevronDown className="h-4 w-4 text-gray-500" />
        )}
      </div>

      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out ${isExpanded ? "max-h-96 mt-2" : "max-h-0"}`}
      >
        <div className="flex flex-wrap gap-1 ml-4">
          {stream.subjects.map((subject, index) => (
            <Badge
              key={`${subject.name}-${index}`}
              variant="outline"
              className="text-[10px] px-1 py-0.5"
            >
              {subject.name}
            </Badge>
          ))}
        </div>
      </div>
    </Card>
  );
};

function EmptyState({
  hasGrades,
  searchTerm,
}: {
  hasGrades: boolean;
  searchTerm: string;
}) {
  return (
    <div className="text-center py-12 text-gray-500">
      <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
      <p>
        {hasGrades && searchTerm !== ""
          ? `No grades match "${searchTerm}"`
          : "No grades added yet. Add your first grade above."}
      </p>
    </div>
  );
}
