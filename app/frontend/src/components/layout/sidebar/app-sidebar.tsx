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

import { getLoggedInUserOptions } from "@/client/@tanstack/react-query.gen";
import { Logout } from "@/components";
import { usePermissions } from "@/components/auth/permission-provider";
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
import { Permission } from "@/lib/permissions";

import type { CurrentUserInfo, PermissionEnum } from "@/client/types.gen";
import type { MainNavItem } from "@/lib/types";

const navigation: MainNavItem = {
  navBar: [
    { title: "Academics", icon: BookOpen, to: "/dashboard/year", permission: Permission["years:read"] },
    { title: "Attendance", icon: Clock, to: "/dashboard" },
    { title: "Analytics", icon: BarChart3, to: "/dashboard" },
    { title: "Communication", icon: MessageSquare, to: "/dashboard" },
    { title: "Finance", icon: DollarSign, to: "/dashboard" },
    { title: "Resources", icon: Layers, to: "/dashboard" },
    { title: "Settings", icon: Cog, to: "/settings" },
  ],
  navMain: [
    {
      title: "People",
      icon: Users,
      isActive: true,
      items: [
        { title: "Students", to: "/dashboard/students", permission: Permission["students:read"] },
        { title: "Teachers", to: "/dashboard/manage-teachers", permission: Permission["teachers:assign"] },
        { title: "Users", to: "/dashboard" },
      ],
    },
    {
      title: "Registration",
      icon: GraduationCap,
      items: [
        { title: "Student Registration", to: "/dashboard/registration/students", permission: Permission["students:write"] },
        { title: "Employee Registration", to: "/dashboard/registration/employees", permission: Permission["employees:write"] },
      ],
    },
    {
      title: "Calendar",
      icon: Calendar,
      items: [{ title: "Events", to: "/dashboard" }],
    },
    {
      title: "Assessments",
      icon: FileText,
      items: [{ title: "Mark List", to: "/dashboard" }],
    },
    {
      title: "Setup",
      icon: Cog,
      items: [
        { title: "Academic Year", to: "/dashboard/year", permission: Permission["years:read"] },
        { title: "Subjects", to: "/dashboard/subjects", permission: Permission["subjects:read"] },
        { title: "Grades", to: "/dashboard/grades", permission: Permission["grades:read"] },
      ],
    },
  ],
};

type AppSidebarProps = React.ComponentProps<typeof Sidebar>;

function filterNavigation(items: MainNavItem, canAccess: (permission?: PermissionEnum) => boolean): MainNavItem {
  return {
    navBar: items.navBar.filter(item => canAccess(item.permission)),
    navMain: items.navMain
      .map(group => ({
        ...group,
        items: group.items.filter(item => canAccess(item.permission)),
      }))
      .filter(group => group.items.length > 0),
  };
}

export default function AppSidebar({ ...props }: AppSidebarProps) {
  const { hasPermission } = usePermissions();
  const { data: currentUserInfo, isLoading } = useQuery(getLoggedInUserOptions());
  const filteredNavigation = filterNavigation(navigation, permission => !permission || hasPermission(permission));

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader className="flex h-14 items-center border-b px-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <Link to="/dashboard" className="flex items-center gap-2 font-semibold">
                <GraduationCap className="h-6 w-6 text-sky-500" />
                <span className="text-xl font-bold text-sky-500">ClassEase</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={filteredNavigation.navMain} />
        <NavSidebar items={filteredNavigation.navBar} />
      </SidebarContent>
      <SidebarFooter className="border-t p-4">
        <FadeIn
          isLoading={isLoading}
          loader={(
            <SidebarFooter className="p-0">
              <div className="flex items-center space-x-2">
                <Skeleton className="h-10 w-10 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-25" />
                  <Skeleton className="h-4 w-17.5" />
                </div>
              </div>
            </SidebarFooter>
          )}
        >
          {currentUserInfo && <UserProfile user={currentUserInfo} />}
        </FadeIn>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}

function initials(name: string) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part.charAt(0).toUpperCase())
    .join("");
}

function UserProfile({ user }: { user: CurrentUserInfo }) {
  const { isMobile } = useSidebar();
  const { activeSchool } = usePermissions();
  const displayName = user.fullName || user.username;

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
                <AvatarImage src={user.imagePath ? user.imagePath : undefined} alt={displayName} />
                <AvatarFallback className="rounded-lg">{initials(displayName)}</AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">{displayName}</span>
                <span className="truncate text-xs font-bold">{activeSchool?.name ?? activeSchool?.slug ?? "No school selected"}</span>
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
                  <AvatarImage src={user.imagePath ? user.imagePath : undefined} alt={displayName} />
                  <AvatarFallback className="rounded-lg">{initials(displayName)}</AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">{displayName}</span>
                  <span className="truncate text-xs">{user.username}</span>
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
            <DropdownMenuItem onSelect={e => e.preventDefault()}>
              <Logout />
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
