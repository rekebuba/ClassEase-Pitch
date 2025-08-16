import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  BookOpen,
  Edit,
  Trash2,
  GraduationCap,
  Users,
  MoreHorizontal,
  Eye,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Subject } from "@/lib/academic-year";

interface SubjectCardProps {
  subject: Subject;
  grades: string[];
  onEdit: () => void;
  onDelete: () => void;
  onView: () => void;
}

export function SubjectCard({
  subject,
  grades,
  onEdit,
  onDelete,
  onView,
}: SubjectCardProps) {
  return (
    <Card
      key={subject.id}
      className="hover:shadow-lg transition-shadow flex flex-col"
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="flex items-center gap-2 mb-2">
              <BookOpen className="h-5 w-5" />
              {subject.name}
            </CardTitle>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => onView(subject)}>
                <Eye className="h-4 w-4 mr-2" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onEdit(subject)}>
                <Edit className="h-4 w-4 mr-2" />
                Edit Subject
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => onDelete(subject)}
                className="text-red-600"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete Subject
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent className="space-y-4 flex-grow">
        {/* Assignment Stats */}
        <div className="grid grid-cols-2 gap-2">
          <div className="text-center p-2 bg-blue-50 rounded-lg">
            <GraduationCap className="h-4 w-4 text-blue-600 mx-auto mb-1" />
            <div className="text-sm font-semibold text-blue-900">
              {grades.length}
            </div>
            <div className="text-xs text-blue-700">Grades</div>
          </div>
          <div className="text-center p-2 bg-purple-50 rounded-lg">
            <Users className="h-4 w-4 text-purple-600 mx-auto mb-1" />
            <div className="text-sm font-semibold text-purple-900">{2}</div>
            <div className="text-xs text-purple-700">Streams</div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex-col items-center gap-2 flex-wrap mt-2">
            <h4 className="text-sm font-medium mb-2">Taught In:</h4>
            <div className="flex flex-wrap gap-1">
              {subject.grades.map((grade) => (
                <Badge key={grade} variant="secondary">
                  Grade {grade}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <div className="flex flex-col gap-2 w-full">
          {/* Last Updated */}
          <div className="text-xs text-gray-500 pt-2 border-t">
            Updated: {new Date().toLocaleDateString()}
          </div>
          {/* Action Buttons */}
          <div className="flex gap-2 bottom-0">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {}}
              className="flex-1 bg-transparent"
            >
              <Eye className="h-4 w-4 mr-2" />
              View
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {}}
              className="flex-1 bg-transparent"
            >
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
