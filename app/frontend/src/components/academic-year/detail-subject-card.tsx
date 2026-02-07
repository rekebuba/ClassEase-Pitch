import { BookOpen } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { SubjectSetupSchema, YearSetupSchemaOutput } from "@/client/types.gen";

type Subject = YearSetupSchemaOutput["subjects"][number];
type Grades = SubjectSetupSchema[];

export default function DetailSubjectCard({
  subject,
  grades,
  children,
}: {
  subject: Subject;
  grades: Grades;
  children?: React.ReactNode;
}) {
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
              {grades.map(grade => (
                <div key={`grade-${grade.id}`}>
                  {grade.hasStream && grade.streams ? (
                    grade.streams
                    // .filter((stream) =>
                    //   stream.subjects.some((s) => s.id === subject.id),
                    // )
                      .map(stream => (
                        <Badge
                          key={`stream-${stream.id}`}
                          variant="default"
                          className="text-xs"
                        >
                          Grade
                          {" "}
                          {grade.grade}
                          {" "}
                          (
                          {stream.name}
                          )
                        </Badge>
                      ))
                  ) : (
                    <Badge
                      key={`grade-only-${grade.id}`}
                      variant="secondary"
                      className="text-xs"
                    >
                      Grade
                      {" "}
                      {grade.grade}
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
