import { Link, useRouterState } from "@tanstack/react-router";
import {
  Bell,
  BookOpenCheck,
  CalendarDays,
  FileClock,
  GraduationCap,
  Palette,
  School,
  ShieldCheck,
} from "lucide-react";

import { cn } from "@/lib/utils";

const settingsNavigation = [
  { title: "General", description: "Identity and contact details", href: "/settings/general", icon: School },
  { title: "Branding", description: "Logo, colors and print assets", href: "/settings/branding", icon: Palette },
  { title: "Academic", description: "Calendar and term defaults", href: "/settings/academic", icon: CalendarDays },
  { title: "Grading", description: "Scales and report options", href: "/settings/grading", icon: GraduationCap },
  { title: "Permissions", description: "Roles and access policy", href: "/settings/permissions", icon: ShieldCheck },
  { title: "Notifications", description: "School communication rules", href: "/settings/notifications", icon: Bell },
  { title: "Audit Logs", description: "Activity and security trail", href: "/settings/audit-logs", icon: FileClock },
];

type SettingsSidebarProps = {
  onNavigate?: () => void;
};

export function SettingsSidebar({ onNavigate }: SettingsSidebarProps) {
  const pathname = useRouterState({ select: state => state.location.pathname });

  return (
    <nav className="space-y-1.5" aria-label="School settings">
      {settingsNavigation.map((item) => {
        const Icon = item.icon;
        const isActive = pathname === item.href || ((pathname === "/settings" || pathname === "/settings/") && item.href === "/settings/general");

        return (
          <Link
            key={item.href}
            to={item.href}
            onClick={onNavigate}
            className={cn(
              "group flex items-start gap-3 rounded-xl px-3 py-3 text-sm transition-colors hover:bg-muted/80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              isActive ? "bg-primary text-primary-foreground shadow-sm hover:bg-primary" : "text-muted-foreground",
            )}
          >
            <Icon className={cn("mt-0.5 size-4 shrink-0", isActive ? "text-primary-foreground" : "text-muted-foreground group-hover:text-foreground")} />
            <span className="min-w-0">
              <span className={cn("block font-medium", isActive ? "text-primary-foreground" : "text-foreground")}>{item.title}</span>
              <span className={cn("mt-0.5 hidden text-xs leading-5 lg:block", isActive ? "text-primary-foreground/80" : "text-muted-foreground")}>{item.description}</span>
            </span>
          </Link>
        );
      })}
      <div className="mt-4 rounded-xl border bg-muted/40 p-3">
        <div className="flex items-center gap-2 text-xs font-medium text-foreground">
          <BookOpenCheck className="size-3.5" />
          Static configuration
        </div>
        <p className="mt-1 text-xs leading-5 text-muted-foreground">
          These controls are ready for backend wiring and do not submit data.
        </p>
      </div>
    </nav>
  );
}

export { settingsNavigation };
