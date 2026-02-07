import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { Bell, Search } from "lucide-react";

import { getYearsOptions } from "@/client/@tanstack/react-query.gen";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useAppDispatch } from "@/hooks/use-store";
import { store } from "@/store/main-store";
import { setYear } from "@/store/slice/year-slice";

export default function AdminHeader() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { data: yearData } = useQuery(getYearsOptions());

  return (
    <header className="sticky top-0 z-30 flex justify-between h-14 items-center gap-4 border-b bg-background px-4 sm:px-6">
      <SidebarTrigger />
      <div className="w-full flex-1 md:w-auto md:flex-none">
        <form>
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search..."
              className="w-full rounded-lg bg-background pl-8 md:w-[200px] lg:w-[300px]"
            />
          </div>
        </form>
      </div>
      <div className="flex items-center gap-2">
        <Select
          defaultValue={store.getState().year.name || yearData?.[0]?.name}
          onValueChange={(value) => {
            const year = yearData?.find(y => y.name === value);
            if (year) {
              dispatch(
                setYear({
                  id: year.id,
                  name: year.name,
                  startDate: year.startDate,
                  endDate: year.endDate,
                  calendarType: year.calendarType,
                }),
              );
              navigate({ to: `/admin` });
            }
          }}
        >
          <SelectTrigger className="w-[280px]">
            <SelectValue placeholder="Select Academic Year" />
          </SelectTrigger>
          <SelectContent>
            {yearData?.map(year => (
              <SelectItem value={year.name}>{year.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon" className="relative">
              <Bell className="h-4 w-4" />
              <Badge className="absolute -right-1 -top-1 h-3 w-3 rounded-full p-0 text-[10px]"></Badge>
              <span className="sr-only">Notifications</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-[300px]">
            <DropdownMenuLabel>Notifications</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <div className="max-h-[300px] overflow-auto">
              {[
                {
                  title: "New student registration",
                  description: "John Smith has registered for 10th grade",
                  time: "5 minutes ago",
                },
                {
                  title: "Staff meeting reminder",
                  description: "Staff meeting at 3:00 PM in Room 101",
                  time: "1 hour ago",
                },
                {
                  title: "System update",
                  description: "ClassEase will be updated tonight at 2:00 AM",
                  time: "3 hours ago",
                },
              ].map((notification, index) => (
                <DropdownMenuItem
                  key={index}
                  className="flex flex-col items-start p-4"
                >
                  <div className="font-medium">{notification.title}</div>
                  <div className="text-sm text-muted-foreground">
                    {notification.description}
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    {notification.time}
                  </div>
                </DropdownMenuItem>
              ))}
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="cursor-pointer justify-center text-center font-medium">
              View all notifications
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
