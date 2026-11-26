import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { clearSession, getStoredSession, login as loginRequest, logout as logoutRequest, storeSession } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const stored = getStoredSession();
  const [user, setUser] = useState(stored?.user || null);
  const [ready, setReady] = useState(true);

  const login = useCallback(async (username, password) => {
    const data = await loginRequest(username, password);
    storeSession(data.token, data.user);
    setUser(data.user);
    return data.user;
  }, []);

  const logout = useCallback(async () => {
    await logoutRequest();
    clearSession();
    setUser(null);
  }, []);

  useEffect(() => {
    function onUnauthorized() {
      setUser(null);
    }
    window.addEventListener("docusearch:unauthorized", onUnauthorized);
    return () => window.removeEventListener("docusearch:unauthorized", onUnauthorized);
  }, []);

  const value = useMemo(
    () => ({
      user,
      ready,
      isAdmin: user?.role === "admin",
      login,
      logout,
    }),
    [user, ready, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth doit être utilisé dans AuthProvider");
  return context;
}
