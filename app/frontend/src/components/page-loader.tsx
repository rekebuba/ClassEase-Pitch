import NProgress from "nprogress";
import "nprogress/nprogress.css";
import { useEffect } from "react";
import { useNavigation } from "react-router-dom";

NProgress.configure({ showSpinner: false });

export default function PageLoader() {
  const navigation = useNavigation();

  useEffect(() => {
    if (navigation.state === "loading") {
      NProgress.start();
    } else {
      NProgress.done();
    }
  }, [navigation.state]);

  return null; // nothing to render, nprogress attaches to <body>
}
