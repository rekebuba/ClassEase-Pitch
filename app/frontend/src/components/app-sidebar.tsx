"use client";

import {
    BarChart3,
    BookOpen,
    Calendar,
    GraduationCap,
    Users,
    FileText,
    MessageSquare,
    Clock,
    Layers,
    DollarSign,
    Award,
    Lightbulb,
    Settings,
    Cog,
} from "lucide-react"
import { Link } from "react-router-dom";
import {
    Sidebar,
    SidebarContent,
    SidebarHeader,
    SidebarFooter,
    SidebarRail,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"

import { useState, useEffect } from "react";
import { NavMain } from "@/components/nav-main"
import { NavSidebar } from "@/components/nav-sidebar"
import { NavUser } from "@/components/nav-user"
import { Skeleton } from "@/components/ui/skeleton"
import { useAuth } from "@/context/auth-context";
import FadeIn from "@/components/fade-in";
import { AdminSchema, StudentSchema, TeacherSchema, UserSchema } from "@/lib/api-response-validation";
import sharedApi from "@/api/sharedApi";
import { toast } from "sonner";
import { z } from "zod";
import { adminApi, studentApi, teacherApi } from "@/api";
import type { Admin, Student, Teacher, User } from "@/lib/api-response-type";
import { pickFields } from "@/utils/pick-zod-fields";
import { useQuery } from "@tanstack/react-query";

const data = {
    admin: {
        system: [
            { title: "Academics", icon: BookOpen, href: "/admin/academics" },
            { title: "Attendance", icon: Clock, href: "/admin/attendance" },
            { title: "Analytics", icon: BarChart3, href: "/admin/analytics" },
            { title: "Communication", icon: MessageSquare, href: "/admin/communication" },
            { title: "Finance", icon: DollarSign, href: "/admin/finance" },
            { title: "Resources", icon: Layers, href: "/admin/resources" },
        ],
        navMain: [
            {
                title: "User Management",
                icon: Users,
                href: "#",
                isActive: true,
                items: [
                    { title: "Manage Students", href: "/admin/manage/students" },
                    { title: "Manage Teachers", href: "/admin/manage/teachers" },
                    { title: "Roles & Permissions", href: "/admin/manage/user-access" }
                ],
            },
            {
                title: "Registration",
                icon: GraduationCap,
                href: "#",
                items: [
                    { title: "Student Registration", href: "/admin/student/applications" },
                    { title: "Teacher Registration", href: "/admin/teacher/applications" }
                ],
            },
            { title: "Calendar", icon: Calendar, href: "#", items: [{ title: "Events", href: "/admin/calendar/events" }] },
            { title: "Assessments", icon: FileText, href: "#", items: [{ title: "Mark List", href: "/admin/assessment/mark-list" }] },
            {
                title: "Setup",
                icon: Cog,
                href: "#",
                items: [
                    { title: "Academic Year", href: "/admin/academic-year-setup" },
                    { title: "Manage Academic Year", href: "/admin/academic-year-manage" },
                ],
            }
        ],
    },
    teacher: {
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
            { title: "Settings", icon: Settings, href: "/teacher/settings" }
        ],
    },
    student: {
        system: [
            { title: "Course Registration", icon: MessageSquare, href: "/student/course/registration" },
            { title: "Schedule", icon: Calendar, href: "#" },
            { title: "Assignments", icon: FileText, href: "#" },
            { title: "Grades", icon: GraduationCap, href: "#" },
            { title: "Courses", icon: BookOpen, href: "#" },
            { title: "Achievements", icon: Award, href: "#" },
            { title: "Classmates", icon: Users, href: "#" }
        ],
        navMain: [
            {
                title: "My Courses",
                icon: BookOpen,
                href: "#",
                isActive: true,
                items: [
                    { title: "Maths", href: "#" },
                    { title: "English", href: "#" },
                    { title: "Science", href: "#" }
                ],
            }
        ]
    }
};

type AppSidebarProps = React.ComponentProps<typeof Sidebar>;

export type PartialUser = Pick<User, "id" | "role" | "identification" | "imagePath">;
export type PartialAdmin = Pick<Admin, "firstName" | "fatherName" | "grandFatherName">;
export type PartialTeacher = Pick<Teacher, "firstName" | "fatherName" | "grandFatherName">;
export type PartialStudent = Pick<Student, "firstName" | "fatherName" | "grandFatherName">;

export function AppSidebar({ ...props }: AppSidebarProps) {
    const { userRole, userId } = useAuth();
    // const [userData, setUserData] = useState<PartialUser | null>(null);
    // const [roleData, setRoleData] = useState<PartialAdmin | PartialStudent | PartialTeacher | null>(null);

    const userFields = ["id", "role", "identification"] as const

    const {
        data: userData,
        isError: isUserError,
        error: userError,
    } = useQuery({
        queryKey: ['user', userId],
        enabled: !!userId,
        queryFn: async () => {
            const selectSchema = pickFields(UserSchema, userFields)
            const res = await sharedApi.getUser(userId!, selectSchema, {
                fields: [...userFields],
            })
            if (!res.success) {
                throw new Error(res.error.message)
            }
            return res.data
        }
    })

    const {
        data: roleData,
        isError: isRoleError,
        error: roleError,
    } = useQuery({
        queryKey: ['role', userRole, userId],
        enabled: !!userId && !!userRole,
        queryFn: async () => {
            const fields = ["id", "firstName", "fatherName", "grandFatherName"] as const

            if (userRole === 'admin') {
                const schema = pickFields(AdminSchema, fields)
                const res = await adminApi.getUser(userId!, schema, { fields: [...fields] })
                if (!res.success) throw new Error(res.error.message)
                return res.data
            }

            if (userRole === 'student') {
                const schema = pickFields(StudentSchema, fields)
                const res = await studentApi.getUser(userId!, schema, { fields: [...fields] })
                if (!res.success) throw new Error(res.error.message)
                return res.data
            }

            if (userRole === 'teacher') {
                const schema = pickFields(TeacherSchema, fields)
                const res = await teacherApi.getUser(userId!, schema, { fields: [...fields] })
                if (!res.success) throw new Error(res.error.message)
                return res.data
            }

            throw new Error('Invalid role')
        }
    })

    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader className="flex h-14 items-center border-b px-4">
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton
                            size="lg"
                            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                        >
                            <Link to={`/${userRole}/dashboard`} className="flex items-center gap-2 font-semibold">
                                <GraduationCap className="h-6 w-6 text-sky-500" />
                                <span className="text-xl font-bold text-sky-500">ClassEase</span>
                            </Link>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                {userRole && (
                    <>
                        <NavMain items={data[userRole].navMain} />
                        <NavSidebar items={data[userRole].system} />
                    </>
                )}
            </SidebarContent>
            <SidebarFooter className="border-t p-4">
                <FadeIn isLoading={!userData} loader={
                    <SidebarFooter className="p-0">
                        <div className="flex items-center space-x-2">
                            <Skeleton className="h-10 w-10 rounded-full" />
                            <div className="space-y-2">
                                <Skeleton className="h-4 w-[100px]" />
                                <Skeleton className="h-4 w-[70px]" />
                            </div>
                        </div>
                    </SidebarFooter>
                }>
                    {(userData && roleData) && <NavUser user={userData} roleData={roleData} />}
                </FadeIn>
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    )
}
