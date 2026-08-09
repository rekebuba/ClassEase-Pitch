import { Link, Outlet, useLocation } from "@tanstack/react-router";
import { BriefcaseBusiness, FileText, GraduationCap, LayoutDashboard, Menu, School, UserRound } from "lucide-react";

import { Logout } from "@/components";
import { useGuest } from "@/components/guest/guest-context";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

const guestNavigation = [
  { label: "Dashboard", to: "/guest", icon: LayoutDashboard },
  { label: "Schools", to: "/guest/schools", icon: School },
  { label: "Jobs", to: "/guest/jobs", icon: BriefcaseBusiness },
  { label: "My Applications", to: "/guest/applications", icon: FileText },
  { label: "Profile", to: "/guest/profile", icon: UserRound },
] as const;

export function GuestLayout() {
  const { profile } = useGuest();
  const displayName = `${profile.firstName} ${profile.lastName}`.trim() || "Guest user";
  const initials = displayName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part.charAt(0).toUpperCase())
    .join("");

  return (
    <div className="min-h-screen bg-slate-50/60">
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <MobileNavigation />
            <Link to="/guest" className="flex items-center gap-2 font-semibold">
              <GraduationCap className="size-6 text-sky-500" />
              <span className="text-xl font-bold text-sky-500">ClassEase</span>
            </Link>
          </div>
          <nav className="hidden items-center gap-1 md:flex">
            {guestNavigation.map(item => <GuestNavLink key={item.to} item={item} />)}
          </nav>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="gap-2 px-2">
                <Avatar className="size-8 rounded-lg">
                  <AvatarFallback className="rounded-lg bg-sky-100 text-sky-700">{initials || "GU"}</AvatarFallback>
                </Avatar>
                <span className="hidden max-w-32 truncate text-sm font-medium sm:block">{displayName}</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>
                <span className="block truncate">{displayName}</span>
                <span className="block truncate text-xs font-normal text-muted-foreground">{profile.email}</span>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link to="/guest/profile">Profile</Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link to="/guest/applications">My Applications</Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onSelect={event => event.preventDefault()}>
                <Logout />
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  );
}

function MobileNavigation() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline" size="icon" className="md:hidden">
          <Menu className="size-4" />
          <span className="sr-only">Open navigation</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-80">
        <SheetHeader>
          <SheetTitle>ClassEase</SheetTitle>
        </SheetHeader>
        <nav className="grid gap-2 px-4">
          {guestNavigation.map(item => <GuestNavLink key={item.to} item={item} mobile />)}
        </nav>
      </SheetContent>
    </Sheet>
  );
}

function GuestNavLink({
  item,
  mobile,
}: {
  item: typeof guestNavigation[number];
  mobile?: boolean;
}) {
  const location = useLocation();
  const active = item.to === "/guest"
    ? location.pathname === "/guest"
    : location.pathname.startsWith(item.to);
  const Icon = item.icon;

  return (
    <Link
      to={item.to}
      className={cn(
        "inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
        active && "bg-sky-50 text-sky-700",
        mobile && "justify-start",
      )}
    >
      <Icon className="size-4" />
      {item.label}
    </Link>
  );
}
