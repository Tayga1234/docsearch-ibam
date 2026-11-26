import { createContext, useContext, useEffect, useMemo, useState } from "react";

export const THEMES = [
  { id: "clair", label: "Clair" },
  { id: "sombre", label: "Sombre" },
  { id: "sahel", label: "Sahel" },
];

const STORAGE_KEY = "docusearch_theme";
const ThemeContext = createContext(null);

function readTheme() {
  const stored = localStorage.getItem(STORAGE_KEY);
  return THEMES.some((theme) => theme.id === stored) ? stored : "clair";
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(readTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  const value = useMemo(
    () => ({
      theme,
      setTheme: setThemeState,
      cycleTheme: () => {
        setThemeState((current) => {
          const index = THEMES.findIndex((item) => item.id === current);
          const next = THEMES[(index + 1) % THEMES.length];
          return next.id;
        });
      },
    }),
    [theme]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme doit être utilisé dans ThemeProvider");
  return context;
}
