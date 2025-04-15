import { RouterProvider } from "react-router-dom";
import router from "./routes/AppRoutes";
import '../src/globals.css';

/**
 * The main application component that sets up the router provider.
 * 
 * This component is responsible for rendering the RouterProvider with the specified router configuration.
 * It serves as the entry point for the application's routing mechanism.
 * 
 * @component
 * @returns {JSX.Element} The RouterProvider component with the configured router.
 */
function App(): JSX.Element {
  return (
      <RouterProvider router={router} />
  );
}

export default App;
