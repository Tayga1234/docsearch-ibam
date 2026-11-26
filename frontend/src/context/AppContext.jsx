import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { checkHealth } from "../services/api";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [apiStatus, setApiStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refreshHealth = useCallback(async () => {
    const data = await checkHealth();
    setApiStatus(data);
    setError(null);
    return data;
  }, []);

  useEffect(() => {
    let cancelled = false;
    refreshHealth()
      .catch((err) => {
        if (!cancelled) {
          setApiStatus(null);
          setError(err.message);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    function onFocus() {
      refreshHealth().catch(() => {});
    }
    window.addEventListener("focus", onFocus);
    return () => {
      cancelled = true;
      window.removeEventListener("focus", onFocus);
    };
  }, [refreshHealth]);

  const value = useMemo(
    () => ({ apiStatus, loading, error, setError, refreshHealth }),
    [apiStatus, loading, error, refreshHealth]
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error("useApp doit être utilisé dans AppProvider");
  return context;
}
