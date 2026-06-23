import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './styles/globals.css'
import './i18n'
import App from './App.tsx'
import { ThemeProvider } from './providers/theme-provider'

import { GoogleOAuthProvider } from '@react-oauth/google'

const queryClient = new QueryClient()
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID || 'your-google-client-id'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider defaultTheme="system" storageKey="kamikonn-ui-theme">
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    </GoogleOAuthProvider>
  </StrictMode>,
)
