import { useNavigate } from "@tanstack/react-router";
import { BookOpen, Calendar, Eye, GraduationCap } from "lucide-react";

import { YearStatusBadge } from "@/components/academic-year";
import AdvanceTooltip from "@/components/advance-tooltip";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatDate } from "@/lib/format";

import type { YearWithRelatedSchema } from "@/client/types.gen";

export default function DetailYearCard({
  academicYear,
}: {
  academicYear: YearWithRelatedSchema;
}) {
  const navigate = useNavigate();

  const getDuration = () => {
    const start = new Date(academicYear.startDate);
    const end = new Date(academicYear.endDate);
    const diffTime = Math.abs(end.getTime() - start.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return `${diffDays} days`;
  };

  return (
    <Card className="w-full hover:shadow-md transition-shadow">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <CardTitle className="text-lg">{academicYear.name}</CardTitle>
              <YearStatusBadge status={academicYear.status} />
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                <span>
                  {formatDate(academicYear.startDate)}
                  {" "}
                  -
                  {" "}
                  {formatDate(academicYear.endDate)}
                </span>
              </div>
              <div className="flex items-center gap-1">
                <span>•</span>
                <span>{getDuration()}</span>
              </div>
              <div className="flex items-center gap-1">
                <span>•</span>
                <span className="capitalize">{academicYear.calendarType}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <AdvanceTooltip
              tooltip="View"
              size="sm"
              onClick={() =>
                navigate({
                  to: `/admin/year/{-$yearId}/year-setup/$yearId/view`,
                  params: { yearId: academicYear.id },
                })}
              className="ml-2"
            >
              <Eye className="h-5 w-5" />
            </AdvanceTooltip>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="flex items-center justify-center mb-1">
              <GraduationCap className="h-5 w-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {academicYear.grades.length}
            </div>
            <div className="text-xs text-blue-600">Grades</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="flex items-center justify-center mb-1">
              <BookOpen className="h-5 w-5 text-green-600" />
            </div>
            <div className="text-2xl font-bold text-green-600">
              {academicYear.subjects.length}
            </div>
            <div className="text-xs text-green-600">Subjects</div>
          </div>
          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-center mb-1">
              <div className="w-5 h-5 bg-purple-600 rounded flex items-center justify-center">
                <span className="text-white text-xs font-bold">T</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-purple-600">
              {academicYear.academicTerms.length}
            </div>
            <div className="text-xs text-purple-600">Terms</div>
          </div>
          <div className="text-center p-3 bg-orange-50 rounded-lg">
            <div className="flex items-center justify-center mb-1">
              <div className="w-5 h-5 bg-orange-600 rounded flex items-center justify-center">
                <span className="text-white text-xs font-bold">E</span>
              </div>
            </div>
            <div className="text-2xl font-bold text-orange-600">
              {academicYear.events.length}
            </div>
            <div className="text-xs text-orange-600">Events</div>
          </div>
        </div>

        <Separator />

        {/* Grades Overview */}
        <div>
          <h4 className="font-medium mb-3 text-sm">Grade Levels</h4>
          <div className="flex flex-wrap gap-2">
            {[...academicYear.grades]
              .sort((a, b) => Number(a.grade) - Number(b.grade))
              .map(grade => (
                <div key={grade.id} className="flex items-center gap-1">
                  <Badge variant="secondary" className="text-xs">
                    Grade
                    {" "}
                    {grade.grade}
                  </Badge>
                </div>
              ))}
          </div>
        </div>

        {/* Subject Categories */}
        <div>
          <h4 className="font-medium mb-3 text-sm">Subjects</h4>
          <div className="flex flex-wrap gap-2">
            {academicYear.subjects.map(subjects => (
              <div key={subjects.id} className="flex items-center gap-1">
                <Badge variant="secondary" className="text-xs">
                  {subjects.name}
                </Badge>
              </div>
            ))}
          </div>
        </div>
        <Separator />

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <div className="text-xs text-gray-500">
            Last updated:
            {" "}
            {formatDate(academicYear.updatedAt)}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
