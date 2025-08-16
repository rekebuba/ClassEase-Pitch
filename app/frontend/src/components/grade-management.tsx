import { YearSetupType } from "@/lib/api-response-type";
import { useFieldArray, UseFormReturn } from "react-hook-form";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
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
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import GradeSetupCard from "./grade-setup-card";
import z from "zod";
import { pickFields } from "@/utils/pick-zod-fields";
import {
  GradeSchema,
  SectionSchema,
  StreamSchema,
  SubjectSchema,
} from "@/lib/api-response-validation";
import { sharedApi } from "@/api";
import { toast } from "sonner";
import { useQueries, useQuery } from "@tanstack/react-query";
import FadeIn from "./fade-in";
import { json } from "stream/consumers";

interface GradeManagementProps {
  form: UseFormReturn<YearSetupType>;
}
type Stream = YearSetupType["grades"][number]["streams"][number];

const GRADE_FIELDS = GradeSchema.keyof().options;
const SECTION_KEYS = SectionSchema.keyof().options;
const SUBJECT_KEYS = SubjectSchema.keyof().options;
const STREAM_KEYS = StreamSchema.keyof().options;

export default function GradeManagement({ form }: GradeManagementProps) {
  // State management
  const [searchTerm, setSearchTerm] = useState("");
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [formMode, setFormMode] = useState<"create" | "edit">("create");
  const [formIndex, setFormIndex] = useState<number>(0);

  // Form field array management
  const {
    fields: gradeFields,
    prepend: prependGrade,
    remove: removeGrade,
  } = useFieldArray({
    control: form.control,
    name: "grades",
    keyName: "rhfId", // Prevents overriding `id`
  });

  const watchForm = form.watch();

  // Memoized fetch function with error handling
  const fetchGrade = useCallback(async (gradeId: string) => {
    try {
      const schema = pickFields(GradeSchema, GRADE_FIELDS).extend({
        sections: z.array(SectionSchema),
        subjects: z.array(SubjectSchema),
        streams: z.array(StreamSchema),
      });

      const response = await sharedApi.getGradeDetail(gradeId, schema, {
        fields: GRADE_FIELDS,
        expand: ["sections", "subjects", "streams"],
        nestedFields: {
          sections: SECTION_KEYS,
          subjects: SUBJECT_KEYS,
          streams: STREAM_KEYS,
        },
      });

      if (!response.success) {
        throw new Error(response.error.message);
      }

      return response.data;
    } catch (error) {
      toast.error("Failed to fetch grade details", {
        description:
          error instanceof Error ? error.message : "Unknown error occurred",
      });
      throw error;
    }
  }, []);

  // Fetch grade details for each grade
  const gradeQueries = useQueries({
    queries: gradeFields.map((grade) => ({
      queryKey: ["grade-detail", grade.id],
      queryFn: () => fetchGrade(grade.id),
      enabled: !!grade.id, // Only fetch if grade has an ID
      staleTime: 5 * 60 * 1000, // 5 minutes cache
    })),
  });

  // Update form values when data is fetched
  useEffect(() => {
    if (gradeQueries.some((q) => q.isFetching)) return;

    gradeQueries.forEach((query, index) => {
      if (query.isSuccess && query.data && index < gradeFields.length) {
        const {
          id,
          grade,
          level,
          yearId,
          hasStream,
          subjects,
          sections,
          streams,
        } = query.data;

        form.setValue(`grades.${index}`, {
          id,
          yearId,
          grade,
          level,
          hasStream,
          subjects: subjects.map(({ id, name, code }) => ({ id, name, code })),
          sections: sections.map(({ id, gradeId, section }) => ({
            id,
            gradeId,
            section,
          })),
          streams: streams.map(({ id, gradeId, name }) => ({
            id,
            gradeId,
            name,
            subjects: [],
          })),
        });
      }
    });
  }, [gradeQueries.every((q) => q.isFetched)]);

  const filteredGrades = watchForm.grades.filter((grade) =>
    grade.grade.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  // Handlers
  const handleCreateGrade = useCallback(() => {
    prependGrade({
      id: crypto.randomUUID(),
      yearId: "",
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

  const handleEditGrade = useCallback((index: number) => {
    setFormMode("edit");
    setFormIndex(index);
    setFormDialogOpen(true);
  }, []);

  const handleRemoveGrade = useCallback(
    (index: number) => {
      removeGrade(index);
      toast.success("Grade removed successfully");
    },
    [removeGrade],
  );

  // Loading state
  const isLoading = gradeQueries.some((query) => query.isLoading);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Grade Levels & Academic Streams</CardTitle>
        <p className="text-sm text-gray-600">
          Configure the grade levels and academic tracks for your school
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search grades..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <Button onClick={() => handleCreateGrade()}>
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredGrades.map((grade, index) => (
            <Card
              key={grade.id}
              className="p-4 hover:shadow-md transition-shadow"
            >
              <CardTitle className="flex items-center gap-2 mb-2">
                <GraduationCap className="text-blue-600" />
                Grade {grade.grade}
                {grade.level && (
                  <Badge className="text-[13px] px-2" variant={"outline"}>
                    {grade.level}
                  </Badge>
                )}
              </CardTitle>
              <div className="flex flex-col gap-4 mb-4 mt-4">
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center p-2 bg-blue-50 rounded-lg">
                    <GraduationCap className="h-4 w-4 text-blue-600 mx-auto mb-1" />
                    <FadeIn
                      isLoading={isLoading}
                      loader={
                        <div className="h-4 w-4 animate-spin border-2 border-blue-500 rounded-full"></div>
                      }
                    >
                      <div className="text-sm font-semibold text-blue-900">
                        {grade.sections.length}
                      </div>
                    </FadeIn>
                    <div className="text-xs text-blue-700">Sections</div>
                  </div>
                  <div className="text-center p-2 bg-purple-50 rounded-lg">
                    <Users className="h-4 w-4 text-purple-600 mx-auto mb-1" />
                    <FadeIn
                      isLoading={isLoading}
                      loader={
                        <div className="h-4 w-4 animate-spin border-2 border-blue-500 rounded-full"></div>
                      }
                    >
                      <div className="text-sm font-semibold text-purple-900">
                        {grade.streams.length}
                      </div>
                    </FadeIn>
                    <div className="text-xs text-purple-700">Streams</div>
                  </div>
                  <div className="text-center p-2 bg-red-50 rounded-lg">
                    <BookOpen className="h-4 w-4 text-red-600 mx-auto mb-1" />
                    <div className="text-sm font-semibold text-red-900">
                      {grade.hasStream
                        ? grade.streams.reduce(
                            (sum, stream) =>
                              sum + (stream.subjects?.length || 0),
                            0,
                          ) + grade.subjects.length
                        : grade.subjects.length}
                    </div>
                    <div className="text-xs text-red-700">Subjects</div>
                  </div>
                </div>
              </div>

              {/* Subject Categories */}
              <div className="mb-4">
                <h4 className="font-medium mb-3 text-sm">Subjects:</h4>
                <div className="mb-4">
                  {grade.streams.map((stream, streamIndex) => (
                    <CollapsibleStreamCard
                      key={streamIndex}
                      form={form}
                      formIndex={index}
                      stream={stream}
                      streamIndex={streamIndex}
                    />
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  {grade.subjects.map((subject) => (
                    <div key={subject.id} className="flex items-center gap-1">
                      <Badge variant="secondary" className="text-xs">
                        {subject.name}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
              <Separator />

              {/* Action Buttons */}
              <div className="flex gap-2 mt-4 flex-wrap">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => removeGrade(index)}
                  className="flex-1 bg-transparent"
                >
                  <Trash className="h-4 w-4 mr-2" />
                  Remove
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 bg-transparent"
                  onClick={() => {
                    setFormMode("edit");
                    setFormIndex(index);
                    setFormDialogOpen(true);
                  }}
                >
                  <Edit className="h-4 w-4 mr-2" />
                  Edit
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </CardContent>

      {filteredGrades.length > 0 && (
        <GradeSetupCard
          form={form}
          open={formDialogOpen}
          onOpenChange={setFormDialogOpen}
          formIndex={formIndex}
          mode={formMode}
        />
      )}
    </Card>
  );
}

interface CollapsibleStreamCardProps {
  form: UseFormReturn<YearSetupType>;
  stream: Stream;
  formIndex: number;
  streamIndex: number;
}

const CollapsibleStreamCard = ({
  form,
  stream,
  formIndex,
  streamIndex,
}: CollapsibleStreamCardProps) => {
  const [isExpanded, setIsExpanded] = useState(true);

  // Memoized fetch function with error handling
  const fetchStream = useCallback(async (streamId: string) => {
    try {
      const schema = z.object({ subjects: z.array(SubjectSchema) });

      const response = await sharedApi.getStreamDetail(streamId, schema, {
        expand: ["subjects"],
        nestedFields: { subjects: SUBJECT_KEYS },
      });

      if (!response.success) {
        throw new Error(response.error.message);
      }

      return response.data;
    } catch (error) {
      toast.error("Failed to fetch grade details", {
        description:
          error instanceof Error ? error.message : "Unknown error occurred",
      });
      throw error;
    }
  }, []);

  // Fetch stream details for each grade
  const streamQueries = useQuery({
    queryKey: ["stream-detail", stream.id],
    queryFn: () => fetchStream(stream.id),
    enabled: !!stream.id, // Only fetch if grade has an ID
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });

  // Update form values when data is fetched
  useEffect(() => {
    if (streamQueries.isFetching) return;

    if (streamQueries.isSuccess && streamQueries.data) {
      const { subjects } = streamQueries.data;

      form.setValue(
        `grades.${formIndex}.streams.${streamIndex}.subjects`,
        subjects,
      );
    }
  }, [streamQueries.isFetching]);

  return (
    <Card className="p-2 bg-gray-50 hover:bg-gray-100 transition-colors border-l-4 border-l-purple-300 mb-3">
      <div
        className="flex items-center justify-between cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-expanded={isExpanded}
        aria-label={`${isExpanded ? "Collapse" : "Expand"} ${stream.name} subjects`}
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Badge className="bg-purple-100 text-black-700 text-xs">
            {stream.name}
          </Badge>
          <Badge className="bg-red-100 text-black-700 text-xs">
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
        className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? "max-h-96 mt-2" : "max-h-0"
        }`}
      >
        <div className="flex flex-wrap gap-1 ml-4">
          {stream.subjects?.map((subject, index) => (
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
        {hasGrades
          ? `No grades match "${searchTerm}"`
          : "No grades added yet. Add your first grade above."}
      </p>
    </div>
  );
}
