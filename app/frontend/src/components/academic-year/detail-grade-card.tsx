import {
  BookOpen,
  Building,
  ChevronDown,
  ChevronUp,
  GraduationCap,
  Layers,
  Users,
} from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { SubjectSchema, YearSetupSchemaOutput } from "@/client/types.gen";

type Subject = SubjectSchema[];
type Grade = YearSetupSchemaOutput["grades"][number];
type Stream = YearSetupSchemaOutput["grades"][number]["streams"][number];

export default function DetailGradeCard({
  grade,
  subjects,
  children,
}: {
  grade: Grade;
  subjects: Subject;
  children?: React.ReactNode;
}) {
  return (
    <Card
      key={grade.id}
      className="flex flex-col justify-between min-h-[260px] p-4 border border-gray-200 hover:shadow-lg transition-shadow"
    >
      <div>
        <CardTitle className="flex items-center gap-2 mb-3 text-lg">
          <GraduationCap className="text-blue-600 shrink-0" />
          Grade
          {" "}
          {grade.grade}
        </CardTitle>
        <div className="flex items-center gap-3 flex-wrap mb-4">
          <Badge variant="outline" className="flex items-center gap-1">
            <Users className="h-3 w-3" />
            {grade.level}
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <BookOpen className="h-3 w-3" />
            {grade.subjects.length}
            {" "}
            Subjects
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <Building className="h-3 w-3" />
            {grade.sections.length}
            {" "}
            Sections
          </Badge>
          {grade.hasStream && (
            <Badge variant="destructive" className="flex items-center gap-1">
              <Layers className="h-3 w-3" />
              {grade.streams.length}
              {" "}
              Streams
            </Badge>
          )}
        </div>

        {/* Subject List */}
        <div className="mb-4">
          <h4 className="font-medium mb-3 text-sm text-gray-600">Subjects</h4>
          {grade.streams?.length === 0 && grade.subjects.length === 0
            ? (
                <p className="text-xs text-gray-400 italic">No subjects assigned</p>
              )
            : (
                <>
                  {grade.hasStream
                    ? (
                        <div className="mb-3 space-y-2">
                          {grade.streams?.map((stream, streamIndex) => (
                            <CollapsibleStreamCard key={streamIndex} stream={stream} />
                          ))}
                        </div>
                      )
                    : (
                        <div className="flex flex-wrap gap-2">
                          {subjects.map(subject => (
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
        <div className="text-xs text-gray-500">
          Last updated:
          {" "}
          {formatDate(grade.updatedAt)}
        </div>
        {children}
      </div>
    </Card>
  );
}

function CollapsibleStreamCard({ stream }: { stream: Stream }) {
  const [isExpanded, setIsExpanded] = useState(false);

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
            {stream.subjects?.length || 0}
            {" "}
            Subjects
          </Badge>
        </div>
        {isExpanded
          ? (
              <ChevronUp className="h-4 w-4 text-gray-500" />
            )
          : (
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
}
