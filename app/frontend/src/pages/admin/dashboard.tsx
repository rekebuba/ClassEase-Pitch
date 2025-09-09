"use client";

import { useState } from "react";
// import { AdminStudentPerformance } from "@/features/admin";
// import { adminApi } from "@/api";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  BookOpen,
  Calendar,
  CheckCircle2,
  Clock,
  Download,
  FileText,
  MoreHorizontal,
  Plus,
  RefreshCw,
  Users,
  XCircle,
} from "lucide-react";

/**
 * AdminDashboard component renders the main dashboard for the admin panel.
 * It fetches and displays an overview of the total number of students and teachers,
 * as well as student performance data.
 */
const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="flex flex-col gap-4 md:gap-8">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back, Principal Powell. Here&apos;s what&apos;s happening at
          your school today.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Students
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,248</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
              <span className="text-emerald-500 font-medium">+5.2%</span> from
              last semester
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Teachers
            </CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">87</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
              <span className="text-emerald-500 font-medium">+2.3%</span> from
              last semester
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Attendance Rate
            </CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94.3%</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
              <span className="text-emerald-500 font-medium">+1.1%</span> from
              last month
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average GPA</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3.42</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowDownRight className="mr-1 h-3 w-3 text-red-500" />
              <span className="text-red-500 font-medium">-0.3%</span> from last
              semester
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs
        defaultValue="overview"
        className="space-y-4"
        onValueChange={setActiveTab}
      >
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="lg:col-span-4">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Student Enrollment by Grade</CardTitle>
                  <CardDescription>
                    Distribution of students across different grades
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm">
                    <Download className="mr-2 h-4 w-4" />
                    Export
                  </Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                        <span className="sr-only">More</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Refresh</DropdownMenuItem>
                      <DropdownMenuItem>View details</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem>Settings</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardHeader>
              <CardContent>
                <div className="h-[300px] w-full">
                  {/* Chart would go here - using placeholder for now */}
                  <div className="flex h-full flex-col items-center justify-center rounded-md border border-dashed p-8 text-center">
                    <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
                      <BarChart3 className="h-10 w-10 text-primary" />
                    </div>
                    <h3 className="mt-4 text-lg font-semibold">
                      Enrollment Chart
                    </h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Bar chart showing student enrollment by grade
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>Average Performance by Subject</CardTitle>
                <CardDescription>
                  Student performance across core subjects
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { subject: "Mathematics", score: 78, change: "+2.4%" },
                    { subject: "Science", score: 82, change: "+1.2%" },
                    { subject: "English", score: 85, change: "+3.1%" },
                    { subject: "History", score: 76, change: "-0.8%" },
                    {
                      subject: "Physical Education",
                      score: 92,
                      change: "+0.5%",
                    },
                  ].map((subject) => (
                    <div key={subject.subject} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{subject.subject}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{subject.score}%</span>
                          <span
                            className={
                              subject.change.startsWith("+")
                                ? "text-emerald-500"
                                : "text-red-500"
                            }
                          >
                            {subject.change}
                          </span>
                        </div>
                      </div>
                      <Progress value={subject.score} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>Upcoming Events</CardTitle>
                <CardDescription>
                  School events for the next 7 days
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      title: "Staff Meeting",
                      date: "Today, 3:00 PM",
                      location: "Conference Room 101",
                      type: "meeting",
                    },
                    {
                      title: "Parent-Teacher Conference",
                      date: "Tomorrow, 4:30 PM",
                      location: "Main Hall",
                      type: "conference",
                    },
                    {
                      title: "Science Fair",
                      date: "Friday, 1:00 PM",
                      location: "Gymnasium",
                      type: "event",
                    },
                    {
                      title: "Basketball Game vs. Westfield",
                      date: "Saturday, 5:00 PM",
                      location: "Sports Complex",
                      type: "sports",
                    },
                  ].map((event, index) => (
                    <div
                      key={index}
                      className="flex items-start gap-4 rounded-lg border p-3"
                    >
                      <div className="rounded-full bg-primary/10 p-2">
                        <Calendar className="h-4 w-4 text-primary" />
                      </div>
                      <div className="flex-1 space-y-1">
                        <p className="font-medium leading-none">
                          {event.title}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {event.date}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {event.location}
                        </p>
                      </div>
                      <Badge
                        variant={
                          event.type === "meeting"
                            ? "outline"
                            : event.type === "conference"
                              ? "secondary"
                              : event.type === "sports"
                                ? "destructive"
                                : "default"
                        }
                      >
                        {event.type}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  <Calendar className="mr-2 h-4 w-4" />
                  View Calendar
                </Button>
              </CardFooter>
            </Card>

            <Card className="lg:col-span-4">
              <CardHeader>
                <CardTitle>Recent Activities</CardTitle>
                <CardDescription>
                  Latest activities across the school
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      user: "Sarah Johnson",
                      action: "added a new student",
                      target: "John Smith to 10th Grade",
                      time: "5 minutes ago",
                      avatar: "/placeholder.svg",
                    },
                    {
                      user: "Michael Chen",
                      action: "updated the curriculum for",
                      target: "Advanced Mathematics",
                      time: "1 hour ago",
                      avatar: "/placeholder.svg",
                    },
                    {
                      user: "Emily Rodriguez",
                      action: "submitted attendance for",
                      target: "9th Grade, Section A",
                      time: "2 hours ago",
                      avatar: "/placeholder.svg",
                    },
                    {
                      user: "David Wilson",
                      action: "created a new event",
                      target: "End of Year Ceremony",
                      time: "Yesterday",
                      avatar: "/placeholder.svg",
                    },
                    {
                      user: "Lisa Thompson",
                      action: "approved budget for",
                      target: "Science Lab Equipment",
                      time: "Yesterday",
                      avatar: "/placeholder.svg",
                    },
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center gap-4">
                      <Avatar className="h-9 w-9">
                        <AvatarImage
                          src={activity.avatar || "/placeholder.svg"}
                          alt={activity.user}
                        />
                        <AvatarFallback>
                          {activity.user
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 space-y-1">
                        <p className="text-sm font-medium leading-none">
                          <span className="font-semibold">{activity.user}</span>{" "}
                          {activity.action}{" "}
                          <span className="font-semibold">
                            {activity.target}
                          </span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  View All Activities
                </Button>
              </CardFooter>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Attendance Alerts</CardTitle>
                <CardDescription>
                  Students with attendance issues
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      name: "Emma Johnson",
                      grade: "10th Grade",
                      absences: 5,
                      status: "warning",
                    },
                    {
                      name: "Tyler Smith",
                      grade: "9th Grade",
                      absences: 8,
                      status: "critical",
                    },
                    {
                      name: "Sophia Garcia",
                      grade: "11th Grade",
                      absences: 4,
                      status: "warning",
                    },
                  ].map((student, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between rounded-lg border p-3"
                    >
                      <div className="flex items-center gap-3">
                        <div className="rounded-full bg-red-100 p-2">
                          {student.status === "critical" ? (
                            <AlertTriangle className="h-4 w-4 text-red-500" />
                          ) : (
                            <Clock className="h-4 w-4 text-amber-500" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium">{student.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {student.grade}
                          </p>
                        </div>
                      </div>
                      <Badge
                        variant={
                          student.status === "critical"
                            ? "destructive"
                            : "outline"
                        }
                      >
                        {student.absences} absences
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  View All Attendance Issues
                </Button>
              </CardFooter>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Academic Performance</CardTitle>
                <CardDescription>
                  Students needing academic support
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      name: "James Wilson",
                      grade: "9th Grade",
                      subject: "Mathematics",
                      score: "65%",
                    },
                    {
                      name: "Olivia Martinez",
                      grade: "11th Grade",
                      subject: "Physics",
                      score: "62%",
                    },
                    {
                      name: "Ethan Brown",
                      grade: "10th Grade",
                      subject: "English",
                      score: "68%",
                    },
                  ].map((student, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between rounded-lg border p-3"
                    >
                      <div className="flex items-center gap-3">
                        <div className="rounded-full bg-amber-100 p-2">
                          <FileText className="h-4 w-4 text-amber-500" />
                        </div>
                        <div>
                          <p className="font-medium">{student.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {student.grade} - {student.subject}
                          </p>
                        </div>
                      </div>
                      <Badge
                        variant="outline"
                        className="text-amber-500 bg-amber-50"
                      >
                        {student.score}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  View All Academic Issues
                </Button>
              </CardFooter>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>Common administrative tasks</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-2">
                  <Button className="justify-start">
                    <Plus className="mr-2 h-4 w-4" />
                    Add New Student
                  </Button>
                  <Button className="justify-start" variant="outline">
                    <Users className="mr-2 h-4 w-4" />
                    Manage Faculty
                  </Button>
                  <Button className="justify-start" variant="outline">
                    <Calendar className="mr-2 h-4 w-4" />
                    Schedule Event
                  </Button>
                  <Button className="justify-start" variant="outline">
                    <FileText className="mr-2 h-4 w-4" />
                    Generate Report
                  </Button>
                  <Button className="justify-start" variant="outline">
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Sync Data
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Advanced Analytics</CardTitle>
              <CardDescription>
                Detailed performance metrics and trends
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                {/* Analytics content would go here */}
                <div className="flex h-full flex-col items-center justify-center rounded-md border border-dashed p-8 text-center">
                  <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
                    <BarChart3 className="h-10 w-10 text-primary" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold">
                    Analytics Dashboard
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Detailed analytics and reporting tools would be displayed
                    here
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Reports</CardTitle>
              <CardDescription>
                Generate and view school reports
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  {
                    title: "Monthly Attendance Report",
                    description: "Summary of student and teacher attendance",
                    date: "Generated on April 1, 2023",
                  },
                  {
                    title: "Academic Performance Report",
                    description: "Analysis of student grades and performance",
                    date: "Generated on March 15, 2023",
                  },
                  {
                    title: "Financial Summary",
                    description: "Overview of budget allocation and expenses",
                    date: "Generated on March 1, 2023",
                  },
                ].map((report, index) => (
                  <div
                    key={index}
                    className="flex items-start justify-between rounded-lg border p-4"
                  >
                    <div className="space-y-1">
                      <h4 className="font-medium">{report.title}</h4>
                      <p className="text-sm text-muted-foreground">
                        {report.description}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {report.date}
                      </p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Download className="mr-2 h-4 w-4" />
                      Download
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>System Notifications</CardTitle>
              <CardDescription>
                Important alerts and notifications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  {
                    title: "System Maintenance",
                    message:
                      "Scheduled maintenance on April 15, 2023 from 2:00 AM to 4:00 AM",
                    type: "info",
                    time: "2 days ago",
                  },
                  {
                    title: "Data Backup Complete",
                    message: "Weekly data backup completed successfully",
                    type: "success",
                    time: "Yesterday",
                  },
                  {
                    title: "Storage Warning",
                    message:
                      "Your storage is at 85% capacity. Consider cleaning up old files.",
                    type: "warning",
                    time: "3 hours ago",
                  },
                  {
                    title: "Failed Login Attempts",
                    message:
                      "Multiple failed login attempts detected from unknown IP address",
                    type: "error",
                    time: "1 hour ago",
                  },
                ].map((notification, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 rounded-lg border p-4"
                  >
                    <div
                      className="rounded-full p-2"
                      style={{
                        backgroundColor:
                          notification.type === "info"
                            ? "rgba(59, 130, 246, 0.1)"
                            : notification.type === "success"
                              ? "rgba(16, 185, 129, 0.1)"
                              : notification.type === "warning"
                                ? "rgba(245, 158, 11, 0.1)"
                                : "rgba(239, 68, 68, 0.1)",
                      }}
                    >
                      {notification.type === "info" && (
                        <Calendar className="h-4 w-4 text-blue-500" />
                      )}
                      {notification.type === "success" && (
                        <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                      )}
                      {notification.type === "warning" && (
                        <AlertTriangle className="h-4 w-4 text-amber-500" />
                      )}
                      {notification.type === "error" && (
                        <XCircle className="h-4 w-4 text-red-500" />
                      )}
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="font-medium">{notification.title}</p>
                        <span className="text-xs text-muted-foreground">
                          {notification.time}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {notification.message}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminDashboard;
