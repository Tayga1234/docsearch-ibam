import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function RequireAuth({ children }) {
  const { user } = useAuth();
  const location = useLocation();
  if (!user) {
    return <Navigate to="/connexion" replace state={{ from: location }} />;
  }
  return children;
}

export function RequireAdmin({ children }) {
  const { user, isAdmin } = useAuth();
  const location = useLocation();
  if (!user) {
    return <Navigate to="/connexion" replace state={{ from: location }} />;
  }
  if (!isAdmin) {
    return <Navigate to="/" replace />;
  }
  return children;
}
