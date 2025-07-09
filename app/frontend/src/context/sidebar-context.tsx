import { RoleEnumType } from "@/lib/enums";
import { createContext, useContext, useState } from "react";


interface AppSidebarContextType {
    role: RoleEnumType;
    isCollapsed: boolean;
    toggleSidebar: () => void;
}

const AppSidebarContext = createContext<AppSidebarContextType | undefined>(undefined);

export function AppSidebarProvider({
    role,
    children
}: {
    role: RoleEnumType;
    children: React.ReactNode
}) {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const toggleSidebar = () => setIsCollapsed(!isCollapsed);

    const value = {
        role,
        isCollapsed,
        toggleSidebar
    };

    return (
        <AppSidebarContext.Provider value={value}>
            {children}
        </AppSidebarContext.Provider>
    );
}

export function useSidebar() {
    const context = useContext(AppSidebarContext);
    if (context === undefined) {
        throw new Error("useSidebar must be used within a AppSidebarProvider");
    }
    return context;
}
