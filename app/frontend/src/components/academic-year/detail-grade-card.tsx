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
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { GradeSetupSchema, GradeStreamSetup } from "@/client/types.gen";

export default function DetailGradeCard({
  grade,
  children,
}: {
  grade: GradeSetupSchema;
  children?: React.ReactNode;
}) {
  const gradeStreams = grade.gradeStreams ?? [];

  const totalSubjects = gradeStreams.reduce(
    (acc, gs) => acc + (gs.subjects?.length ?? 0),
    0,
  );

  const plainSubjects = !grade.hasStream
    ? gradeStreams.flatMap(gs => gs.subjects ?? [])
    : [];

  return (
    <Card className="flex flex-col justify-between min-h-64 p-4 border border-gray-200 hover:shadow-lg transition-shadow">
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
            {totalSubjects}
            {" "}
            Subjects
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <Building className="h-3 w-3" />
            {grade.sections?.length ?? 0}
            {" "}
            Sections
          </Badge>
          {grade.hasStream && (
            <Badge variant="destructive" className="flex items-center gap-1">
              <Layers className="h-3 w-3" />
              {gradeStreams.length}
              {" "}
              Streams
            </Badge>
          )}
        </div>

        {/* Subject List */}
        <div className="mb-4">
          <h4 className="font-medium mb-3 text-sm text-gray-600">Subjects</h4>
          {gradeStreams.length === 0 || totalSubjects === 0
            ? (
                <p className="text-xs text-gray-400 italic">No subjects assigned</p>
              )
            : grade.hasStream
              ? (
                  <div className="mb-3 space-y-2">
                    {gradeStreams.map((gs, i) => {
                      return (
                        <CollapsibleStreamCard
                          key={i}
                          stream={gs}
                          index={i}
                        />
                      );
                    })}
                  </div>
                )
              : (
                  <div className="flex flex-wrap gap-2">
                    {plainSubjects.map(subject => (
                      <Badge key={subject.id} variant="secondary" className="text-xs">
                        {subject.name}
                      </Badge>
                    ))}
                  </div>
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

function CollapsibleStreamCard({ stream, index }: { stream: GradeStreamSetup; index: number }) {
  const [isOpen, setIsOpen] = useState(index === 0); // Open the first stream by default
  const subjects = stream.subjects ?? [];

  return (
    <Collapsible
      open={isOpen}
      onOpenChange={setIsOpen}
      className="rounded-md border-l-4 border-l-purple-300 bg-gray-50 p-2 hover:bg-gray-100 transition-colors mb-2"
    >
      <CollapsibleTrigger asChild>
        <button
          type="button"
          className="flex w-full items-center justify-between focus:outline-none focus:ring-1 focus:ring-purple-400 rounded p-1 text-left"
          aria-label={`${isOpen ? "Collapse" : "Expand"} ${
            stream.stream?.name ?? "General"
          } subjects`}
        >
          <div className="flex gap-2">
            <Badge variant="outline" className="bg-purple-100 text-gray-800 text-xs font-normal">
              {stream.stream?.name ?? "General"}
            </Badge>
            <Badge variant="outline" className="bg-red-100 text-gray-800 text-xs font-normal">
              {subjects.length}
              {" "}
              Subjects
            </Badge>
          </div>
          {isOpen
            ? (
                <ChevronUp className="h-4 w-4 text-gray-500 transition-transform duration-200" />
              )
            : (
                <ChevronDown className="h-4 w-4 text-gray-500 transition-transform duration-200" />
              )}
        </button>
      </CollapsibleTrigger>

      <CollapsibleContent className="data-[state=open]:animate-collapsible-down data-[state=closed]:animate-collapsible-up overflow-hidden transition-all">
        <div className="flex flex-wrap gap-1 ml-2 pt-2">
          {subjects.map(subject => (
            <Badge
              key={subject.id}
              variant="outline"
              className="text-[10px] px-1.5 py-0.5 bg-white font-normal text-gray-700"
            >
              {subject.name}
            </Badge>
          ))}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
