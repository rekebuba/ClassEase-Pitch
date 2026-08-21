import {
  BarChart3,
  BookOpen,
  BriefcaseBusiness,
  Building2,
  Calendar,
  ClipboardCheck,
  Clock,
  Cog,
  DollarSign,
  FileArchive,
  FileText,
  GraduationCap,
  Layers,
  MessageSquare,
  ScrollText,
  UserCheck,
  Users,
} from "lucide-react";

import { Permission } from "@/lib/permissions";

import type { MainNavItem, NavBarItem, NavMainItem } from "@/lib/types";
import type { PermissionEnum } from "@/client/types.gen";

export const navigation: MainNavItem = {
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
      title: "HR Management",
      icon: BriefcaseBusiness,
      items: [
        { title: "Dashboard", icon: BarChart3, to: "/dashboard/hr" },
        { title: "Employees", icon: UserCheck, to: "/dashboard/hr/employees" },
        { title: "Departments", icon: Building2, to: "/dashboard/hr/departments" },
        { title: "Positions", icon: ClipboardCheck, to: "/dashboard/hr/positions" },
        {
          title: "Recruitment",
          icon: BriefcaseBusiness,
          to: "/dashboard/hr/recruitment",
          items: [
            { title: "Job Postings", to: "/dashboard/hr/recruitment/jobs" },
            { title: "Applications", to: "/dashboard/hr/recruitment/applications" },
          ],
        },
        { title: "Leave", icon: Calendar, to: "/dashboard/hr/leave" },
        { title: "Attendance", icon: Clock, to: "/dashboard/hr/attendance" },
        { title: "Performance", icon: ScrollText, to: "/dashboard/hr/performance" },
        { title: "Documents", icon: FileArchive, to: "/dashboard/hr/documents" },
        { title: "Reports", icon: FileText, to: "/dashboard/hr/reports" },
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

function canAccessItem<T extends { permission?: PermissionEnum; items?: NavBarItem[] }>(
  item: T,
  canAccess: (permission?: PermissionEnum) => boolean,
): T | null {
  if (!canAccess(item.permission)) {
    return null;
  }

  if (!item.items) {
    return item;
  }

  const items = item.items
    .map(child => canAccessItem(child, canAccess))
    .filter((child): child is NavBarItem => Boolean(child));

  if (items.length === 0 && !("to" in item && item.to)) {
    return null;
  }

  return { ...item, items };
}

export function filterNavigation(items: MainNavItem, canAccess: (permission?: PermissionEnum) => boolean): MainNavItem {
  return {
    navBar: items.navBar
      .map(item => canAccessItem(item, canAccess))
      .filter((item): item is NavBarItem => Boolean(item)),
    navMain: items.navMain
      .map(item => canAccessItem(item, canAccess))
      .filter((item): item is NavMainItem => Boolean(item)),
  };
}
