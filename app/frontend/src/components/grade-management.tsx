import { YearSetupType } from "@/lib/api-response-type";
import { useFieldArray, UseFormReturn } from "react-hook-form";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { BookOpen, ChevronDown, ChevronUp, Edit, GraduationCap, Plus, Search, Trash, Users } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useState } from "react";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import GradeSetupCard from "./grade-setup-card";

interface GradeManagementProps {
    form: UseFormReturn<YearSetupType>
}
type Stream = YearSetupType["grades"][number]["streams"][number];

export default function GradeManagement({ form }: GradeManagementProps) {
    const [searchTerm, setSearchTerm] = useState("")
    const [formDialogOpen, setFormDialogOpen] = useState(false)
    const [formMode, setFormMode] = useState<"create" | "edit">("create")
    const [formIndex, setFormIndex] = useState<number>(0)


    const { fields: gradeFields, prepend: prependGrade, remove: removeGrade, } = useFieldArray({
        control: form.control,
        name: "grades",
    })
    const watchForm = form.watch()

    const filteredGrades = watchForm.grades.filter((grade) => grade.grade.toLowerCase().includes(searchTerm.toLowerCase()))

    const handleCreateGrade = () => {
        prependGrade({
            id: "",
            yearId: "",
            grade: "",
            level: "" as "primary",
            hasStream: false,
            streams: [],
            sections: [],
            subjects: [],
        }); // Add empty grade
        setFormMode("create");
        setFormIndex(0); // Always edit the first grade in the list
        setFormDialogOpen(true);
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Grade Levels & Academic Streams</CardTitle>
                <p className="text-sm text-gray-600">Configure the grade levels and academic tracks for your school</p>
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

                {filteredGrades.length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                        <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                        <p>
                            {gradeFields.length === 0
                                ? "No grades added yet. Add your first grade above."
                                : "No grades match your search criteria."}
                        </p>
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredGrades.map((grade, index) => (
                        <Card key={grade.id} className="p-4 hover:shadow-md transition-shadow">
                            <CardTitle className="flex items-center gap-2 mb-2">
                                <GraduationCap className="text-blue-600" />
                                {grade.grade}
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
                                        <div className="text-sm font-semibold text-blue-900">{grade.sections.length}</div>
                                        <div className="text-xs text-blue-700">Sections</div>
                                    </div>
                                    <div className="text-center p-2 bg-purple-50 rounded-lg">
                                        <Users className="h-4 w-4 text-purple-600 mx-auto mb-1" />
                                        <div className="text-sm font-semibold text-purple-900">{grade.streams.length}</div>
                                        <div className="text-xs text-purple-700">Streams</div>
                                    </div>
                                    <div className="text-center p-2 bg-red-50 rounded-lg">
                                        <BookOpen className="h-4 w-4 text-red-600 mx-auto mb-1" />
                                        <div className="text-sm font-semibold text-red-900">
                                            {grade.hasStream ? grade.streams.reduce(
                                                (sum, stream) => sum + (stream.subjects?.length || 0),
                                                0
                                            ) : grade.subjects.length}
                                        </div>
                                        <div className="text-xs text-red-700">Subjects</div>
                                    </div>
                                </div>
                            </div>

                            {/* Subject Categories */}
                            <div className="mb-4">
                                <h4 className="font-medium mb-3 text-sm">Subjects:</h4>
                                {!grade.hasStream ? (
                                    <div className="flex flex-wrap gap-2">
                                        {grade.subjects.map((subject) => (
                                            <div key={subject.id} className="flex items-center gap-1">
                                                <Badge variant="secondary" className="text-xs">
                                                    {subject.name}
                                                </Badge>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="mb-4">
                                        {grade.streams.map((stream, streamIndex) => (
                                            <CollapsibleStreamCard key={streamIndex} stream={stream} />
                                        ))}
                                    </div>
                                )}
                            </div>
                            <Separator />

                            {/* Action Buttons */}
                            <div className="flex gap-2 mt-4 flex-wrap">
                                <Button variant="outline" size="sm" onClick={() => removeGrade(index)} className="flex-1 bg-transparent">
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
                                    }}>
                                    <Edit className="h-4 w-4 mr-2" />
                                    Edit
                                </Button>
                            </div>
                        </Card>
                    ))}
                </div>
            </CardContent>

            {filteredGrades.length > 0 &&
                <GradeSetupCard
                    form={form}
                    open={formDialogOpen}
                    onOpenChange={setFormDialogOpen}
                    formIndex={formIndex}
                    mode={formMode}
                />
            }
        </Card>
    );
}


const CollapsibleStreamCard = ({ stream }: { stream: Stream }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <Card className="p-2 bg-gray-50 hover:bg-gray-100 transition-colors border-l-4 border-l-purple-300 mb-3">
            <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => setIsExpanded(!isExpanded)}
                aria-expanded={isExpanded}
                aria-label={`${isExpanded ? 'Collapse' : 'Expand'} ${stream.name} subjects`}
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
                className={`overflow-hidden transition-all duration-300 ease-in-out ${isExpanded ? 'max-h-96 mt-2' : 'max-h-0'
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
