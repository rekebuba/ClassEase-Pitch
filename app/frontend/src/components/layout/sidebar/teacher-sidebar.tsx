import { Logout } from "@/components";
import FadeIn from "@/components/fade-in";
import { NavMain } from "@/components/nav-main";
import { NavSidebar } from "@/components/nav-sidebar";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  useSidebar,
} from "@/components/ui/sidebar";
import { Skeleton } from "@/components/ui/skeleton";
import { useAppSelector } from "@/hooks/use-store";
import { api, TeacherInfo } from "@/store/api";
import { Link } from "@tanstack/react-router";
import {
  Award,
  BadgeCheck,
  BarChart3,
  Bell,
  Calendar,
  ChevronsUpDown,
  Clock,
  CreditCard,
  FileText,
  GraduationCap,
  Layers,
  Lightbulb,
  Settings,
  Sparkles,
  Users,
} from "lucide-react";

const data = {
  navMain: [],
  system: [
    { title: "Students", icon: Users, href: "/teacher/students" },
    { title: "Assignments", icon: FileText, href: "/teacher/assignments" },
    { title: "Grades", icon: Award, href: "/teacher/grades" },
    { title: "Attendance", icon: Clock, href: "/teacher/attendance" },
    { title: "Calendar", icon: Calendar, href: "/teacher/calendar" },
    { title: "Resources", icon: Layers, href: "/teacher/resources" },
    { title: "Analytics", icon: BarChart3, href: "/teacher/analytics" },
    { title: "Insights", icon: Lightbulb, href: "/teacher/insights" },
    { title: "Settings", icon: Settings, href: "/teacher/settings" },
  ],
};

type TeacherSidebarProps = React.ComponentProps<typeof Sidebar>;

export default function TeacherSidebar({ ...props }: TeacherSidebarProps) {
  const { token } = useAppSelector((state) => state.auth);
  const { data: teacherInfo, isLoading } = api.useGetTeacherBasicInfoQuery(
    undefined,
    {
      skip: !token,
    },
  );

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader className="flex h-14 items-center border-b px-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <Link
                to={`/teacher`}
                className="flex items-center gap-2 font-semibold"
              >
                <GraduationCap className="h-6 w-6 text-sky-500" />
                <span className="text-xl font-bold text-sky-500">
                  ClassEase
                </span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavSidebar items={data.system} />
      </SidebarContent>
      <SidebarFooter className="border-t p-4">
        <FadeIn
          isLoading={isLoading}
          loader={
            <SidebarFooter className="p-0">
              <div className="flex items-center space-x-2">
                <Skeleton className="h-10 w-10 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[100px]" />
                  <Skeleton className="h-4 w-[70px]" />
                </div>
              </div>
            </SidebarFooter>
          }
        >
          {teacherInfo && <TeacherProfile user={teacherInfo} />}
        </FadeIn>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}

function TeacherProfile({ user }: { user: TeacherInfo }) {
  const teacher = user.teacher;
  const { isMobile } = useSidebar();

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage
                  src={user.imagePath ? user.imagePath : undefined}
                  alt={teacher.firstName}
                />
                {teacher.firstName && teacher.fatherName && (
                  <AvatarFallback className="rounded-lg">
                    {teacher.firstName.charAt(0).toUpperCase() +
                      teacher.fatherName.charAt(0).toUpperCase()}
                  </AvatarFallback>
                )}
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">
                  Mr. {teacher.firstName} {teacher.fatherName}
                </span>
                <span className="truncate text-xs font-bold">{user.role}</span>
              </div>
              <ChevronsUpDown className="ml-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage
                    src={user.imagePath ? user.imagePath : undefined}
                    alt={teacher.firstName}
                  />
                  {teacher.firstName && teacher.fatherName && (
                    <AvatarFallback className="rounded-lg">
                      {teacher.firstName.charAt(0).toUpperCase() +
                        teacher.fatherName.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  )}
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">
                    Mr. {teacher.firstName} {teacher.fatherName}{" "}
                    {teacher.grandFatherName}
                  </span>
                  <span className="truncate text-xs">
                    {user.identification}
                  </span>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <Sparkles />
                Upgrade to Pro
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <BadgeCheck />
                Account
              </DropdownMenuItem>
              <DropdownMenuItem>
                <CreditCard />
                Billing
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Bell />
                Notifications
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
              <Logout />
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
