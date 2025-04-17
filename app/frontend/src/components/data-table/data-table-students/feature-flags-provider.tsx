"use client";

import { useSearchParams, useNavigate } from "react-router-dom";
import * as React from "react";

import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { type FlagConfig, flagConfig } from "@/config/flag";

type FilterFlag = FlagConfig["featureFlags"][number]["value"];

interface FeatureFlagsContextValue {
  filterFlag: FilterFlag | null;
  enableAdvancedFilter: boolean;
}

const FeatureFlagsContext =
  React.createContext<FeatureFlagsContextValue | null>(null);

export function useFeatureFlags() {
  const context = React.useContext(FeatureFlagsContext);
  if (!context) {
    throw new Error(
      "useFeatureFlags must be used within a FeatureFlagsProvider",
    );
  }
  return context;
}

interface FeatureFlagsProviderProps {
  children: React.ReactNode;
}

export function FeatureFlagsProvider({ children }: FeatureFlagsProviderProps) {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // Get filterFlag from URL
  const filterFlag = React.useMemo(() => {
    const value = searchParams.get("filterFlag");
    if (!value) return null;
    const validValues = flagConfig.featureFlags.map((flag) => flag.value);
    return validValues.includes(value as FilterFlag)
      ? (value as FilterFlag)
      : null;
  }, [searchParams]);

  const onFilterFlagChange = React.useCallback(
    (value: string) => {
      const newSearchParams = new URLSearchParams(searchParams);
      if (value) {
        newSearchParams.set("filterFlag", value);
      } else {
        newSearchParams.delete("filterFlag");
      }
      setSearchParams(newSearchParams, { replace: true });
    },
    [searchParams, setSearchParams]
  );

  const contextValue = React.useMemo<FeatureFlagsContextValue>(
    () => ({
      filterFlag,
      enableAdvancedFilter:
        filterFlag === "advancedFilters" || filterFlag === "commandFilters",
    }),
    [filterFlag],
  );

  return (
    <FeatureFlagsContext.Provider value={contextValue}>
      <div className="w-full overflow-x-auto p-1">
        <ToggleGroup
          type="single"
          variant="outline"
          size="sm"
          value={filterFlag || ""}
          onValueChange={onFilterFlagChange}
          className="w-fit gap-0"
        >
          {flagConfig.featureFlags.map((flag) => (
            <Tooltip key={flag.value} delayDuration={700}>
              <ToggleGroupItem
                value={flag.value}
                className="whitespace-nowrap px-3 text-xs data-[state=on]:bg-accent/70 data-[state=on]:hover:bg-accent/90"
                asChild
              >
                <TooltipTrigger>
                  <flag.icon className="size-3.5 shrink-0" />
                  {flag.label}
                </TooltipTrigger>
              </ToggleGroupItem>
              <TooltipContent
                align="start"
                side="bottom"
                sideOffset={6}
                className="flex flex-col gap-1.5 border bg-background py-2 font-semibold text-foreground [&>span]:hidden"
              >
                <div>{flag.tooltipTitle}</div>
                <p className="text-balance text-muted-foreground text-xs">
                  {flag.tooltipDescription}
                </p>
              </TooltipContent>
            </Tooltip>
          ))}
        </ToggleGroup>
      </div>
      {children}
    </FeatureFlagsContext.Provider>
  );
}
