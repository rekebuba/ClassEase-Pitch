import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import RootLayout from "./RootLayout";
import App from './App.jsx';


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RootLayout>
      <App />
    </RootLayout>
  </StrictMode>,
)
