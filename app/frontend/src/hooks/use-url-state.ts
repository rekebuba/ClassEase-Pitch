"use client";

import { useMemo } from "react";
import { useLocation } from "react-router-dom";

export function useQueryParams() {
  const location = useLocation();
  return useMemo(() => {
    const params = new URLSearchParams(location.search);
    return Object.fromEntries(params.entries());
  }, [location.search]);
}
