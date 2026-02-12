import * as React from "react";
import { useEffect, useState } from "react";

type FadeInProps = {
  children: React.ReactNode;
  isLoading: boolean;
  loader: React.ReactNode;
};

const FadeIn: React.FC<FadeInProps> = ({ children, isLoading, loader }) => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      // eslint-disable-next-line react-hooks-extra/no-direct-set-state-in-use-effect
      setIsLoaded(true);
    }
  }, [isLoading]);

  if (isLoading) {
    return <>{loader}</>;
  }

  return <div className={isLoaded ? "fade-in" : ""}>{children}</div>;
};

export default FadeIn;
