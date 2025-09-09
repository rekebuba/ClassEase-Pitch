import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { type NavBarItem } from "@/lib/types";
import { Link } from "@tanstack/react-router";
import { JSX } from "react";

export function NavSidebar({ items }: { items: NavBarItem[] }): JSX.Element {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Reports</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton asChild>
              <Link
                key={item.to}
                to={item.to}
                params={item.params}
                search={item.search}
                className="flex items-center gap-2 p-2 hover:bg-gray-100"
              >
                <span>{item.title}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  );
}
