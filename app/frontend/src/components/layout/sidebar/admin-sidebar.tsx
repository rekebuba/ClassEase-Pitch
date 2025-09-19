import { getAdminBasicInfoOptions } from "@/client/@tanstack/react-query.gen";
import { AdminInfo } from "@/client/types.gen";
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
import { MainNavItem } from "@/lib/types";
import { store } from "@/store/main-store";
import { useQuery } from "@tanstack/react-query";
import { Link } from "@tanstack/react-router";
import {
  BadgeCheck,
  BarChart3,
  Bell,
  BookOpen,
  Calendar,
  ChevronsUpDown,
  Clock,
  Cog,
  CreditCard,
  DollarSign,
  FileText,
  GraduationCap,
  Layers,
  MessageSquare,
  Sparkles,
  Users,
} from "lucide-react";

const data: MainNavItem = {
  navBar: [
    { title: "Academics", icon: BookOpen, to: "/admin/academics" },
    { title: "Attendance", icon: Clock, to: "/admin/attendance" },
    { title: "Analytics", icon: BarChart3, to: "/admin/analytics" },
    {
      title: "Communication",
      icon: MessageSquare,
      to: "/admin/communication",
    },
    { title: "Finance", icon: DollarSign, to: "/admin/finance" },
    { title: "Resources", icon: Layers, to: "/admin/resources" },
  ],
  navMain: [
    {
      title: "User Management",
      icon: Users,
      isActive: true,
      items: [
        { title: "Manage Students", to: "/admin/manage/students" },
        { title: "Manage Teachers", to: "/admin/manage/teachers" },
        { title: "Roles & Permissions", to: "/admin/manage/user-access" },
      ],
    },
    {
      title: "Registration",
      icon: GraduationCap,
      items: [
        {
          title: "Student Registration",
          to: `/admin/registration/students`,
        },
        {
          title: "Employee Registration",
          to: `/admin/registration/employees`,
        },
      ],
    },
    {
      title: "Calendar",
      icon: Calendar,
      items: [{ title: "Events", to: "/admin/calendar/events" }],
    },
    {
      title: "Assessments",
      icon: FileText,
      items: [{ title: "Mark List", to: "/admin/assessment/mark-list" }],
    },
    {
      title: "Setup",
      icon: Cog,
      items: [
        {
          title: "Academic Year",
          to: `/admin/year`,
        },
        {
          title: "Subjects",
          to: `/admin/subjects`,
        },
        {
          title: "Grades",
          to: `/admin/grades`,
        },
      ],
    },
  ],
};

type AdminSidebarProps = React.ComponentProps<typeof Sidebar>;

export default function AdminSidebar({ ...props }: AdminSidebarProps) {
  const state = store.getState();
  const { data: adminInfo, isLoading } = useQuery(getAdminBasicInfoOptions());

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
                to={`/admin`}
                params={{ yearId: state.year.id }}
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
        <NavSidebar items={data.navBar} />
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
          {adminInfo && <AdminProfile user={adminInfo} />}
        </FadeIn>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}

function AdminProfile({ user }: { user: AdminInfo }) {
  const admin = user.admin;
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
                  alt={admin.firstName}
                />
                {admin.firstName && admin.fatherName && (
                  <AvatarFallback className="rounded-lg">
                    {admin.firstName.charAt(0).toUpperCase() +
                      admin.fatherName.charAt(0).toUpperCase()}
                  </AvatarFallback>
                )}
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">
                  Mr. {admin.firstName} {admin.fatherName}
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
                    alt={admin.firstName}
                  />
                  {admin.firstName && admin.fatherName && (
                    <AvatarFallback className="rounded-lg">
                      {admin.firstName.charAt(0).toUpperCase() +
                        admin.fatherName.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  )}
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">
                    Mr. {admin.firstName} {admin.fatherName}{" "}
                    {admin.grandFatherName}
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
