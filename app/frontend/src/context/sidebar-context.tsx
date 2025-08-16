import { RoleType } from "@/lib/enums";
import { createContext, useContext, useState } from "react";

interface AppSidebarContextType {
  role: RoleType;
  isCollapsed: boolean;
  toggleSidebar: () => void;
}

const AppSidebarContext = createContext<AppSidebarContextType | undefined>(
  undefined,
);

export function AppSidebarProvider({
  role,
  children,
}: {
  role: RoleType;
  children: React.ReactNode;
}) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => setIsCollapsed(!isCollapsed);

  const value = {
    role,
    isCollapsed,
    toggleSidebar,
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
