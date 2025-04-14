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
import { sharedApi } from '@/api';

import { NavMain } from "@/components/layout/nav-main"
import { NavSidebar } from "@/components/layout/nav-sidebar"
import { NavUser } from "@/components/layout/nav-user"
// import { title } from "process";

const data = {
    admin: {
        user: {
            firstName: "Example",
            fatherName: "Example",
            grandFatherName: "Example",
            email: "m@example.com",
            role: "Example",
        },
        system: [
            {
                title: "Academics",
                icon: BookOpen,
                href: "/admin/academics",
            },
            {
                title: "Attendance",
                icon: Clock,
                href: "/admin/attendance",
            },
            {
                title: "Analytics",
                icon: BarChart3,
                href: "/admin/analytics",
            },
            {
                title: "Communication",
                icon: MessageSquare,
                href: "/admin/communication",
            },
            {
                title: "Finance",
                icon: DollarSign,
                href: "/admin/finance",
            },
            {
                title: "Resources",
                icon: Layers,
                href: "/admin/resources",
            },
        ],
        navMain: [
            {
                title: "User Management",
                icon: Users,
                href: "#",
                isActive: true,
                items: [
                    {
                        title: "Manage Students",
                        href: "/admin/manage/students",
                    },
                    {
                        title: "Manage Teachers",
                        href: "/admin/manage/teachers",
                    },
                    {
                        title: "Roles & Permissions",
                        href: "/admin/manage/user-access",
                    }
                ],
            },
            {
                title: "Registration",
                icon: GraduationCap,
                href: "#",
                items: [
                    {
                        title: "Student Registration",
                        href: "/admin/student/registration",
                    },
                    {
                        title: "Teacher Registration",
                        href: "/admin/teacher/registration",
                    }
                ],
            },
            {
                title: "Calendar",
                icon: Calendar,
                href: "#",
                items: [
                    {
                        title: "Events",
                        href: "/admin/calendar/events",
                    }
                ],
            },
            {
                title: "Assessments",
                icon: FileText,
                href: "#",
                items: [
                    {
                        title: "Mark List",
                        href: "/admin/assessment/mark-list",
                    }
                ],
            },
        ],
    },
    teacher: {
        user: {
            firstName: "Example",
            fatherName: "Example",
            grandFatherName: "Example",
            email: "m@example.com",
            role: "Example",
        },
        system: [
            {
                title: "Students",
                icon: Users,
                href: "/teacher/students",
            },
            {
                title: "Assignments",
                icon: FileText,
                href: "/teacher/assignments",
            },
            {
                title: "Grades",
                icon: Award,
                href: "/teacher/grades",
            },
            {
                title: "Attendance",
                icon: Clock,
                href: "/teacher/attendance",
            },
            {
                title: "Calendar",
                icon: Calendar,
                href: "/teacher/calendar",
            },
            {
                title: "Resources",
                icon: Layers,
                href: "/teacher/resources",
            },
            {
                title: "Analytics",
                icon: BarChart3,
                href: "/teacher/analytics",
            },
            {
                title: "Insights",
                icon: Lightbulb,
                href: "/teacher/insights",
            },
            {
                title: "Settings",
                icon: Settings,
                href: "/teacher/settings",
            }
        ],
    },
    student: {
        user: {
            firstName: "Example",
            fatherName: "Example",
            grandFatherName: "Example",
            email: "m@example.com",
            role: "Example",
        },
        system: [
            {
                title: "Course Registration",
                icon: MessageSquare,
                href: "/student/course/registration",
            },
            {
                title: "Schedule",
                icon: Calendar,
                href: "#"
            },
            {
                title: "Assignments",
                icon: FileText,
                href: "#"
            },
            {
                title: "Grades",
                icon: GraduationCap,
                href: "#"
            },
            {
                title: "Courses",
                icon: BookOpen,
                href: "#"
            },
            {
                title: "Achievements",
                icon: Award,
                href: "#"
            },
            {
                title: "Classmates",
                icon: Users,
                href: "#"
            },
        ],
        navMain: [
            {
                title: "My Courses",
                icon: BookOpen,
                href: "#",
                isActive: true,
                items: [
                    {
                        title: "Maths",
                        href: "#",
                    },
                    {
                        title: "English",
                        href: "#",
                    },
                    {
                        title: "Science",
                        href: "#",
                    }
                ],
            }
        ]
    }
}

export function AppSidebar({ role, ...props }) {
    const [userData, setUserData] = useState(data[role].user);

    /**
     * @hook useEffect
     * @description Fetches user data from the server when the component mounts.
     * @param {Function} fetchUser - Fetches user data from the server.
     */
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await sharedApi.getUser();
                const flattenedData = {
                    ...response.data['user'],
                    ...response.data['detail'],
                };
                setUserData(flattenedData);

            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    console.error(error.response.data['error']);
                }
                return;
            }
        };
        fetchUser();
    }, []);

    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader className="flex h-14 items-center border-b px-4">
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton
                            size="lg"
                            aria-title="Go to Dashboard"
                            className="data-[state=open]:bg-sidebar-accent
                            data-[state=open]:text-sidebar-accent-foreground"
                        >
                            <Link to={`/${role}/dashboard`} className="flex items-center gap-2 font-semibold">
                                <GraduationCap className="h-6 w-6 text-sky-500" />
                                <span className="text-xl font-bold text-sky-500">ClassEase</span>
                            </Link>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                {data[role].navMain && <NavMain items={data[role].navMain} />}
                {data[role].system && <NavSidebar items={data[role].system} />}
            </SidebarContent>
            <SidebarFooter className="border-t p-4">
                <NavUser user={{ ...userData }} />
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    )
}
