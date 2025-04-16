"use client";

import { ErrorPage } from "@/components/ui/error-page";

/**
 * NotFound Component
 * 
 * This functional component renders a 404 error message indicating that the requested page was not found.
 * It displays a sad face emoji followed by the text "404, page not found."
 * 
 * @component
 * @example
 * return (
 *   <NotFound />
 * )
 * 
 * @returns {JSX.Element} A JSX element containing the 404 error message.
 */
const NotFound = () => {
  return (
    <ErrorPage
      statusCode={404}
      title="Page Not Found"
      description="Sorry, we couldn't find the page you're looking for. The page might have been moved, deleted, or never existed."
      actions={{
        primary: {
          label: "Back to Home",
          href: "/",
        },
        secondary: {
          label: "Go Back",
          onClick: () => window.history.back(),
        },
      }}
    />
  )
}


export default NotFound;
