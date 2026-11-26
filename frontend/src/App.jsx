import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "./components/AppShell";
import { RequireAdmin } from "./components/RequireAuth";
import { AppProvider } from "./context/AppContext";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import DocumentPage from "./pages/DocumentPage";
import DocumentsPage from "./pages/DocumentsPage";
import HelpPage from "./pages/HelpPage";
import IngestPage from "./pages/IngestPage";
import LibraryPage from "./pages/LibraryPage";
import LoginPage from "./pages/LoginPage";
import NotFoundPage from "./pages/NotFoundPage";
import SearchPage from "./pages/SearchPage";
import StatusPage from "./pages/StatusPage";
import "./App.css";

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppProvider>
          <Routes>
            <Route path="/connexion" element={<LoginPage />} />
            <Route element={<AppShell />}>
              <Route index element={<SearchPage />} />
              <Route path="fonds" element={<LibraryPage />} />
              <Route path="documents/:id" element={<DocumentPage />} />
              <Route path="systeme" element={<StatusPage />} />
              <Route path="aide" element={<HelpPage />} />
              <Route
                path="documents"
                element={
                  <RequireAdmin>
                    <DocumentsPage />
                  </RequireAdmin>
                }
              />
              <Route
                path="indexation"
                element={
                  <RequireAdmin>
                    <IngestPage />
                  </RequireAdmin>
                }
              />
              <Route path="recherche" element={<Navigate to="/" replace />} />
              <Route path="*" element={<NotFoundPage />} />
            </Route>
          </Routes>
        </AppProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}
