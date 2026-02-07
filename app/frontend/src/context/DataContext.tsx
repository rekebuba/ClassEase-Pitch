import React, { createContext, useContext, useState } from "react";

const DataContext = createContext();

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState(null);

  return (
    <DataContext.Provider value={{ data, setData }}>
      {children}
    </DataContext.Provider>
  );
}

export const useData = () => useContext(DataContext);
