import * as React from "react";

type FadeInProps = {
  children: React.ReactNode;
  isLoading: boolean;
  loader: React.ReactNode;
};

const FadeIn: React.FC<FadeInProps> = ({ children, isLoading, loader }) => {
  if (isLoading) {
    return <>{loader}</>;
  }

  return <div className="fade-in">{children}</div>;
};

export default FadeIn;
