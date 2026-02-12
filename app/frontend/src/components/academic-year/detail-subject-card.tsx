import { BookOpen } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { SubjectSetupSchema } from "@/client/types.gen";

export default function DetailSubjectCard({
  subject,
  grades,
  children,
}: {
  subject: SubjectSetupSchema;
  grades: SubjectSetupSchema["grades"];
  children?: React.ReactNode;
}) {
  const gradesWithStreams = (gradeId: string) => {
    return subject.streams.filter(stream => stream.gradeId === gradeId).map(stream => stream.name.charAt(0)).join(", ");
  };

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
          {subject.grades.length > 0 || subject.streams.length > 0
            ? (
                <div className="flex flex-wrap gap-2">
                  {grades.map((grade) => {
                    const streams = gradesWithStreams(grade.id);
                    return (
                      <Badge
                        key={`grade-only-${grade.id}`}
                        variant="secondary"
                        className="text-xs"
                      >
                        Grade&nbsp;
                        {grade.grade}
                        {grade.hasStream && streams && (
                          <p className="text-xs text-amber-600">
                            &nbsp;
                            (
                            {streams}
                            )
                          </p>
                        )}
                      </Badge>
                    );
                  })}
                </div>
              )
            : (
                <p className="text-xs text-gray-400 italic">No grades assigned</p>
              )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2">
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
