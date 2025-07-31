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
import { UserSchema, type UserProfile } from "@/lib/api-response-validation";
import sharedApi, { getDashboardData } from "@/api/sharedApi";
import { toast } from "sonner";
import { z } from "zod";

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

function pickFields<T extends z.ZodRawShape>(
    schema: z.ZodObject<T>,
    fields: (keyof T)[]
): z.ZodObject<Pick<T, (keyof T & string)>> {
    const shape = Object.fromEntries(
        fields.map((key) => [key, schema.shape[key]])
    ) as Pick<T, (keyof T & string)>;
    return z.object(shape);
}

export function AppSidebar({ ...props }: AppSidebarProps) {
    const [userData, setUserData] = useState<UserProfile | null>(null);
    const { userRole, userId } = useAuth();


    useEffect(() => {
        const fetchUserData = async () => {
            if (!userRole || !userId) return; // Prevent rendering if userRole is not set
            const selectedSchema = pickFields(UserSchema, ["id", "role", "imagePath"]);

            const response = await sharedApi.getUser(userId, selectedSchema);

            if (!response.success) {
                toast.error(response.error.message, {
                    style: { color: "red" },
                });
                return;
            }
            setUserData(response.data);
        };

        fetchUserData();
    }, [userRole, userId]);

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
                <FadeIn isLoading={!userRole} loader={<SidebarSkeleton {...props} />}>
                    {userRole && (
                        <>
                            <NavMain items={data[userRole].navMain} />
                            <NavSidebar items={data[userRole].system} />
                        </>
                    )}
                </FadeIn>
            </SidebarContent>
            <SidebarFooter className="border-t p-4">
                <FadeIn isLoading={!userData} loader={<SidebarSkeleton {...props} />}>
                    {userData && <NavUser user={userData} />}
                </FadeIn>
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    )
}

function SidebarSkeleton({ ...props }) {
    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader className="flex h-14 items-center border-b px-4">
                <Skeleton className="h-8 w-32" />
            </SidebarHeader>
            <SidebarContent>
                <div className="space-y-4 p-4">
                    <Skeleton className="h-8 w-full" />
                    <Skeleton className="h-8 w-full" />
                    <Skeleton className="h-8 w-full" />
                </div>
            </SidebarContent>
            <SidebarFooter className="border-t p-4">
                <div className="flex items-center space-x-4">
                    <Skeleton className="h-10 w-10 rounded-full" />
                    <div className="space-y-2">
                        <Skeleton className="h-4 w-[100px]" />
                        <Skeleton className="h-4 w-[70px]" />
                    </div>
                </div>
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    );
}
