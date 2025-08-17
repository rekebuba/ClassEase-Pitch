import {
  BasicInfoTab,
  GradesTab,
  SubjectsTab,
} from "@/components/academic-year/tabs";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BookOpen, Calendar, GraduationCap } from "lucide-react";

export function AcademicYearTabs({
  activeTab,
  onTabChange,
  onUnsavedChange,
}: {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onUnsavedChange: (dirty: boolean) => void;
}) {
  return (
    <Tabs value={activeTab} onValueChange={onTabChange}>
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="basic" className="flex items-center gap-2">
          <Calendar className="h-4 w-4" />
          Basic Info
        </TabsTrigger>
        <TabsTrigger value="subjects" className="flex items-center gap-2">
          <BookOpen className="h-4 w-4" />
          Subjects
        </TabsTrigger>
        <TabsTrigger value="grades" className="flex items-center gap-2">
          <GraduationCap className="h-4 w-4" />
          Grades & Streams
        </TabsTrigger>
      </TabsList>

      <TabsContent value="basic">
        <BasicInfoTab onDirty={onUnsavedChange} />
      </TabsContent>
      <TabsContent value="subjects">
        <SubjectsTab onDirty={onUnsavedChange} />
      </TabsContent>
      <TabsContent value="grades">
        <GradesTab onDirty={onUnsavedChange} />
      </TabsContent>
    </Tabs>
  );
}
