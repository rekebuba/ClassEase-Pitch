import { BookOpen } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { GradeSchema, StreamSchema, SubjectSetupSchema } from "@/client/types.gen";

type GroupedGrade = {
  grade: GradeSchema;
  streams: StreamSchema[];
};

export default function DetailSubjectCard({
  subject,
  children,
}: {
  subject: SubjectSetupSchema;
  children?: React.ReactNode;
}) {
  const gradeStreams = subject.gradeStreams ?? [];

  // Group streams by Grade ID
  const groupedGrades = gradeStreams.reduce<Record<string, GroupedGrade>>((acc, gs) => {
    const gradeId = gs.grade.id;
    if (!acc[gradeId]) {
      acc[gradeId] = {
        grade: gs.grade,
        streams: [],
      };
    }
    if (gs.stream) {
      acc[gradeId].streams.push(gs.stream);
    }
    return acc;
  }, {});

  const gradeList = Object.values(groupedGrades);

  return (
    <Card className="flex flex-col justify-between min-h-56 p-4 border border-gray-200 hover:shadow-lg transition-shadow">
      {/* Title */}
      <div>
        <CardTitle className="flex items-center gap-2 mb-3 text-base">
          <BookOpen className="text-blue-600 shrink-0 h-5 w-5" />
          <span className="truncate">{subject.name}</span>
          <Badge className="text-[12px] px-2 font-normal" variant="outline">
            {subject.code}
          </Badge>
        </CardTitle>

        {/* Grades */}
        <div className="mt-3">
          <h4 className="font-medium mb-3 text-sm text-gray-600">Taught In</h4>
          {gradeList.length === 0
            ? (
                <p className="text-xs text-gray-400 italic">No grades assigned</p>
              )
            : (
                <div className="flex flex-wrap gap-2">
                  {gradeList.map(({ grade, streams }) => {
                    const streamLetters = streams.map(s => s.name.charAt(0)).join(", ");
                    const hasStreams = grade.hasStream && streamLetters.length > 0;

                    return (
                      <Badge
                        key={grade.id}
                        variant="secondary"
                        className="text-xs font-normal flex items-center gap-1"
                      >
                        <span>
                          Grade
                          {" "}
                          {grade.grade}
                        </span>
                        {hasStreams && (
                          <span className="text-amber-600 font-medium">
                            (
                            {streamLetters}
                            )
                          </span>
                        )}
                      </Badge>
                    );
                  })}
                </div>
              )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2 mt-4">
        <Separator />
        <div className="text-xs text-gray-500">
          Last updated:
          {" "}
          {formatDate(subject.updatedAt)}
        </div>
        {children}
      </div>
    </Card>
  );
}
