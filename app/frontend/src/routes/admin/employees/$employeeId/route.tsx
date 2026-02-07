import { useQuery } from "@tanstack/react-query";
import {
  createFileRoute,
  Link,
  Outlet,
  useRouter,
} from "@tanstack/react-router";
import { motion, useScroll, useTransform } from "framer-motion";
import {
  BookOpen,
  Calendar,
  Clock,
  Edit,
  FileText,
  Info,
  Mail,
  Phone,
} from "lucide-react";
import { useRef } from "react";

import {
  getEmployeeOptions,
} from "@/client/@tanstack/react-query.gen";
import AdvanceTooltip from "@/components/advance-tooltip";
import EmployeeApplicationStatusBadge from "@/components/enum-badge/employee-application-status-badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { formatDate } from "@/lib/format";
import { cn } from "@/lib/utils";
import { getInitials } from "@/utils/utils";

import type { MainNavItem } from "@/lib/types";

export const Route = createFileRoute("/admin/employees/$employeeId")({
  component: RouteComponent,
});

function SimpleSidebarNavigation() {
  const router = useRouter();
  const employeeId = Route.useParams().employeeId;

  if (!employeeId)
    return null;

  const contentNav: MainNavItem = {
    navBar: [
      {
        title: "Profile",
        icon: Info,
        to: "/admin/employees/$employeeId/profile",
        params: { employeeId },
      },
      {
        title: "Schedule",
        icon: BookOpen,
        to: "/admin/employees/$employeeId/schedule",
        params: { employeeId },
      },
      {
        title: "Interview",
        icon: BookOpen,
        to: "/admin/employees/$employeeId/interview",
        params: { employeeId },
      },
      {
        title: "Notes",
        icon: FileText,
        to: "/admin/employees/$employeeId/notes",
        params: { employeeId },
      },
    ],
    navMain: [],
  };

  return (
    <nav className="space-y-1">
      {contentNav.navBar.map((item) => {
        const isActive = router.state.location.pathname === item.to;

        return (
          <AdvanceTooltip
            size="lg"
            tooltip={item.title}
            key={item.title}
            className={cn(
              "bg-transparent border-none font-semibold flex w-full items-center justify-center md:justify-start gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
              "hover:bg-muted hover:text-foreground",
              isActive
                ? "bg-muted text-foreground shadow-sm"
                : "text-muted-foreground",
            )}
            side="right"
            asChild
          >
            <Link
              to={item.to}
              params={item.params}
              search={item.search}
              className="flex items-center gap-3 no-underline"
            >
              {item.icon && <item.icon />}
              <span className="hidden md:inline-block truncate">
                {item.title}
              </span>
            </Link>
          </AdvanceTooltip>
        );
      })}
    </nav>
  );
}

function RouteComponent() {
  // const yearId = store.getState().year.id;
  // const navigate = useNavigate();
  const employeeId = Route.useParams().employeeId;

  const { data: employee } = useQuery({
    ...getEmployeeOptions({
      path: { employee_id: employeeId },
    }),
    enabled: !!employeeId,
  });

  // const updateEmployeeStatus = useMutation({
  //   ...updateEmployeeStatusMutation(),
  //   onSuccess: (success) => {
  //     toast.success(success.message, {
  //       style: { color: "green" },
  //     });
  //     queryClient.invalidateQueries({
  //       queryKey: getEmployeeQueryKey({
  //         path: { employee_id: employeeId },
  //       }),
  //     });
  //     navigate({ to: "/admin/registration/employees" });
  //   },
  //   onError: () => {
  //     toast.error("Something went wrong.", { style: { color: "red" } });
  //   },
  // });

  // const onStatusChange = (newStatus: Status) => {
  //   updateEmployeeStatus.mutate({
  //     body: { yearId: yearId!, status: newStatus, employeeIds: [employeeId] },
  //   });
  // };

  const scrollRef = useRef(null);
  const { scrollYProgress } = useScroll({
    container: scrollRef,
  });

  // Smoothly shrink header height and avatar size
  const headerHeight = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["160px", "80px"],
  );
  const avatarSize = useTransform(scrollYProgress, [0, 0.2], ["6rem", "3rem"]);
  const nameFont = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["1.875rem", "1.125rem"],
  );
  const detailsOpacity = useTransform(scrollYProgress, [0, 0.15], [1, 0]);
  const shadowOpacity = useTransform(scrollYProgress, [0, 0.05], [0, 1]);
  const roleFontSize = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["0.875rem", "0.75rem"],
  );
  const profileInfoGap = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["0.75rem", "0.25rem"],
  );
  const nameSectionAlign = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["flex-start", "center"],
  );
  const nameSectionGap = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["0px", "0.5rem"],
  );
  const roleOpacity = useTransform(scrollYProgress, [0, 0.2], [1, 0.8]);
  const detailsHeight = useTransform(
    scrollYProgress,
    [0, 0.15],
    ["auto", "0px"],
  );
  const detailsMarginTop = useTransform(
    scrollYProgress,
    [0, 0.15],
    ["0.5rem", "0rem"],
  );

  // New transforms for layout adjustments
  const contentGap = useTransform(
    scrollYProgress,
    [0, 0.2],
    ["1.5rem", "0.75rem"],
  ); // gap-6 -> gap-3
  const boxShadow = useTransform(
    shadowOpacity,
    value => `0 2px 8px rgba(0,0,0,${value * 0.1})`,
  );

  if (!employee)
    return null;

  return (
    <Card className="border-none h-screen flex flex-col overflow-hidden">
      {/* Animated Sticky Header */}
      <motion.div
        style={{
          height: headerHeight,
          boxShadow,
        }}
        className="sticky bg-white z-20 flex items-center px-6 top-0"
      >
        <div className="flex justify-between w-full items-center">
          <motion.div
            style={{ gap: contentGap }}
            className="flex gap-6 justify-between items-center flex-1"
          >
            <motion.div
              style={{
                width: avatarSize,
                height: avatarSize,
              }}
              className="flex-shrink-0 justify-between items-center"
            >
              <Avatar className="w-full h-full">
                <AvatarImage src={undefined} />
                <AvatarFallback className="bg-primary/10 text-primary font-semibold text-xl">
                  {getInitials(employee.firstName, employee.fatherName)}
                </AvatarFallback>
              </Avatar>
            </motion.div>

            <motion.div
              style={{ gap: profileInfoGap }}
              className="flex flex-col min-w-0 flex-1"
            >
              <motion.div
                style={{ alignItems: nameSectionAlign, gap: nameSectionGap }}
                className="flex items-center min-w-0"
              >
                <motion.h1
                  style={{ fontSize: nameFont }}
                  className="font-bold text-foreground truncate mr-2"
                >
                  {employee.firstName}
                  {" "}
                  {employee.fatherName}
                </motion.h1>
                <EmployeeApplicationStatusBadge status={employee.status} />
              </motion.div>
              <motion.p
                style={{ fontSize: roleFontSize, opacity: roleOpacity }}
                className=" font-bold text-muted-foreground truncate m-0"
              >
                {employee.subject?.name}
                {" "}
                Teacher
              </motion.p>

              <motion.div
                style={{
                  opacity: detailsOpacity,
                  height: detailsHeight,
                  marginTop: detailsMarginTop,
                  overflow: "hidden",
                }}
                className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm"
              >
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Mail className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">{employee.personalEmail}</span>
                </div>
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Phone className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">{employee.primaryPhone}</span>
                </div>
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Calendar className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">
                    Hired:
                    {" "}
                    {formatDate(employee.createdAt)}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Clock className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">
                    {employee.yearsOfExperience}
                    {" "}
                    years experience
                  </span>
                </div>
              </motion.div>
            </motion.div>
          </motion.div>

          <Button className="bg-primary hover:bg-primary/90 shrink-0">
            <Edit className="w-4 h-4 md:mr-2" />
            <span className="hidden md:inline-block">Edit Profile</span>
          </Button>
        </div>
      </motion.div>

      <div className="flex flex-1 overflow-hidden">
        <motion.div
          style={{ top: headerHeight }}
          className="w-16 border-r p-2 sticky left-0 self-start h-[calc(100vh-var(--header-height))] overflow-y-auto bg-white transition-all duration-300 ease-in-out"
        >
          <SimpleSidebarNavigation />
        </motion.div>

        {/* Scrollable Outlet */}
        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50"
        >
          <Outlet />
        </div>
      </div>
    </Card>
  );
}
