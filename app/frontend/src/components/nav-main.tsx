import { Link, useRouter } from "@tanstack/react-router";
import { ChevronRight } from "lucide-react";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";

import type { NavMainItem } from "@/lib/types";
import type { NavBarItem } from "@/lib/types";
import type { JSX } from "react";

function isActivePath(pathname: string, to?: string) {
  return Boolean(to && (pathname === to || pathname.startsWith(`${to}/`)));
}

function NavSubTree({ items, pathname, depth = 0 }: { items: NavBarItem[]; pathname: string; depth?: number }) {
  return (
    <SidebarMenuSub>
      {items.map((subItem) => {
        const hasChildren = Boolean(subItem.items?.length);
        const active = isActivePath(pathname, subItem.to);

        return (
          <SidebarMenuSubItem key={subItem.title}>
            {hasChildren
              ? (
                  <Collapsible defaultOpen={active} className="group/sub-collapsible">
                    <CollapsibleTrigger asChild>
                      <SidebarMenuSubButton className="w-full">
                        {subItem.icon && <subItem.icon />}
                        <span>{subItem.title}</span>
                        <ChevronRight className="ml-auto h-4 w-4 transition-transform duration-200 group-data-[state=open]/sub-collapsible:rotate-90" />
                      </SidebarMenuSubButton>
                    </CollapsibleTrigger>
                    <CollapsibleContent className={depth > 0 ? "pl-3" : undefined}>
                      <NavSubTree items={subItem.items ?? []} pathname={pathname} depth={depth + 1} />
                    </CollapsibleContent>
                  </Collapsible>
                )
              : (
                  <SidebarMenuSubButton asChild isActive={active}>
                    <Link
                      to={subItem.to}
                      key={subItem.to}
                      params={subItem.params}
                      search={subItem.search}
                      className="flex items-center gap-2 p-2 hover:bg-gray-100"
                    >
                      {subItem.icon && <subItem.icon />}
                      <span>{subItem.title}</span>
                    </Link>
                  </SidebarMenuSubButton>
                )}
          </SidebarMenuSubItem>
        );
      })}
    </SidebarMenuSub>
  );
}

export function NavMain({ items }: { items: NavMainItem[] }): JSX.Element {
  const router = useRouter();
  const pathname = router.state.location.pathname;

  return (
    <SidebarGroup>
      <SidebarGroupLabel>System</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => {
          const active = item.to ? isActivePath(pathname, item.to) : item.items?.some(child => isActivePath(pathname, child.to));

          return (
          <Collapsible
            key={item.title}
            asChild
            defaultOpen={item.isActive || active}
            className="group/collapsible"
          >
            <SidebarMenuItem>
              <CollapsibleTrigger asChild>
                <SidebarMenuButton tooltip={item.title} isActive={active}>
                  {item.icon && <item.icon />}
                  <span>{item.title}</span>
                  <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                </SidebarMenuButton>
              </CollapsibleTrigger>
              <CollapsibleContent>
                {item.items && <NavSubTree items={item.items} pathname={pathname} />}
              </CollapsibleContent>
            </SidebarMenuItem>
          </Collapsible>
          );
        })}
      </SidebarMenu>
    </SidebarGroup>
  );
}
