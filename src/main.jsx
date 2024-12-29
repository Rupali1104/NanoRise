import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ClerkProvider } from '@clerk/clerk-react';

// This is your public Clerk key - it's safe to include directly since it's public
const CLERK_KEY = 'pk_test_cGF0aWVudC1raW5nZmlzaC00Mi5jbGVyay5hY2NvdW50cy5kZXYk';

// Use environment variable if available, otherwise use the hardcoded key
const clerk_key = import.meta.env.VITE_CLERK_KEY || CLERK_KEY;

// Remove the error check since we now have a fallback
if(!clerk_key){
  throw new Error("Key was not found");
}

createRoot(document.getElementById('root')).render(
 <StrictMode>
   <ClerkProvider publishableKey={clerk_key}>
     <App />
   </ClerkProvider>
 </StrictMode>,
)