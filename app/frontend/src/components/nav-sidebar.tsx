import {
    SidebarGroup,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import { type NavItem } from "@/lib/types"
import { useLocation, useNavigate } from "react-router-dom";

export function NavSidebar({ items }: { items: NavItem[] }): JSX.Element {
    const location = useLocation();

    const navigate = useNavigate();

    const goToSideBar = (href: string) => {
        navigate(`${href}${location.search}`);
    }

    return (
        <SidebarGroup>
            <SidebarGroupLabel>Reports</SidebarGroupLabel>
            <SidebarMenu>
                {items.map((item) => (
                    <SidebarMenuItem key={item.title}>
                        <SidebarMenuButton asChild>
                            <a onClick={() => goToSideBar(item.href)}>
                                <span>{item.title}</span>
                            </a>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                ))}
            </SidebarMenu>
        </SidebarGroup>
    )
}
