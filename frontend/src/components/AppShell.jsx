import { useEffect, useState } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
import { useApp } from "../context/AppContext";
import { useAuth } from "../context/AuthContext";
import BackButton from "./BackButton";
import ThemeSwitch from "./ThemeSwitch";

const GROUPS = [
  {
    id: "public",
    label: "Espace public",
    links: [
      {
        to: "/",
        label: "Recherche",
        end: true,
        public: true,
        icon: ["M10.5 18a7.5 7.5 0 1 1 0-15 7.5 7.5 0 0 1 0 15Z", "M16.6 16.6 21 21"],
      },
      {
        to: "/fonds",
        label: "Fonds",
        public: true,
        icon: ["M6 8h12v11H6z", "M8 8V6.5A1.5 1.5 0 0 1 9.5 5h5A1.5 1.5 0 0 1 16 6.5V8"],
      },
      {
        to: "/systeme",
        label: "Système",
        public: true,
        icon: ["M12 4v4", "M12 16v4", "M4 12h4", "M16 12h4", "M12 12m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0-5 0"],
      },
      {
        to: "/aide",
        label: "Aide",
        public: true,
        icon: ["M12 19h.01", "M9.2 9a2.8 2.8 0 1 1 4.3 2.4c-.8.6-1.5 1.1-1.5 2.2"],
      },
    ],
  },
  {
    id: "admin",
    label: "Administration",
    links: [
      {
        to: "/documents",
        label: "Documents",
        adminOnly: true,
        icon: ["M7 4h8l4 4v12H7z", "M15 4v4h4"],
      },
      {
        to: "/indexation",
        label: "Indexation",
        adminOnly: true,
        icon: ["M12 4v11", "M8 11l4 4 4-4", "M6 19h12"],
      },
    ],
  },
];

function pageMeta(pathname) {
  if (pathname.startsWith("/indexation")) return { kicker: "Administration", title: "Indexation" };
  if (pathname.startsWith("/systeme")) return { kicker: "Supervision", title: "Système" };
  if (pathname.startsWith("/aide")) return { kicker: "Guide", title: "Aide" };
  if (/^\/documents\/[^/]+/.test(pathname)) return { kicker: "Collection", title: "Fiche" };
  if (pathname.startsWith("/documents")) return { kicker: "Administration", title: "Documents" };
  if (pathname.startsWith("/fonds")) return { kicker: "Collection", title: "Fonds" };
  return { kicker: "Espace public", title: "Recherche" };
}

function initials(name) {
  const parts = String(name || "")
    .split(" ")
    .filter(Boolean)
    .slice(0, 2);
  if (parts.length === 0) return "?";
  return parts.map((part) => part[0]).join("").toUpperCase();
}

function isMobileLayout() {
  return window.matchMedia("(max-width: 860px)").matches;
}

function NavIcon({ paths }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      {paths.map((d) => (
        <path
          key={d}
          d={d}
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
    </svg>
  );
}

export default function AppShell() {
  const { error, setError, apiStatus, refreshHealth } = useApp();
  const { user, isAdmin, logout } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(() => !isMobileLayout());
  const visibleGroups = GROUPS.map((group) => ({
    ...group,
    links: group.links.filter((link) => link.public || (link.adminOnly && isAdmin)),
  })).filter((group) => group.links.length > 0);
  const indexedCount = apiStatus?.documents;
  const meta = pageMeta(location.pathname);
  const apiOnline = Boolean(apiStatus);

  useEffect(() => {
    refreshHealth().catch(() => {});
  }, [location.pathname, refreshHealth]);

  useEffect(() => {
    if (isMobileLayout()) setSidebarOpen(false);
  }, [location.pathname]);

  function toggleSidebar() {
    setSidebarOpen((open) => !open);
  }

  function closeIfMobile() {
    if (isMobileLayout()) setSidebarOpen(false);
  }

  return (
    <div className={`shell ${sidebarOpen ? "" : "is-collapsed"}`}>
      <aside className={`sidebar ${sidebarOpen ? "is-open" : ""}`}>
        <div className="sidebar-brand">
          <img src="/docusearch-logo.png" alt="" width={40} height={40} />
          <div>
            <strong>DocSearch</strong>
            <span>IBAM · Archives</span>
          </div>
        </div>
        <span className={`sidebar-role ${isAdmin ? "is-admin" : ""}`}>
          {isAdmin ? "Administrateur" : "Espace public"}
        </span>

        <nav className="sidebar-nav">
          {visibleGroups.map((group) => (
            <div key={group.id} className="sidebar-group">
              <p className="sidebar-label">{group.label}</p>
              {group.links.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.end}
                  className={({ isActive }) => `nav-link ${isActive ? "is-active" : ""}`}
                  onClick={closeIfMobile}
                >
                  <NavIcon paths={link.icon} />
                  {link.label}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-foot">
          <div className={`sidebar-status ${apiOnline ? "is-online" : "is-offline"}`}>
            <span className="status-dot" />
            <div>
              <strong>{apiOnline ? "API en ligne" : "API hors ligne"}</strong>
              <small>
                {typeof indexedCount === "number" ? `${indexedCount} documents` : "Index…"}
              </small>
            </div>
          </div>
          <p className="sidebar-hint">Touche / pour chercher</p>
        </div>
      </aside>

      {sidebarOpen && (
        <button type="button" className="sidebar-backdrop" onClick={toggleSidebar} />
      )}

      <div className="shell-main">
        <header className="topbar">
          <div className="topbar-left">
            <button
              type="button"
              className={`icon-btn sidebar-toggle ${sidebarOpen ? "is-open" : ""}`}
              onClick={toggleSidebar}
              aria-label={sidebarOpen ? "Masquer le menu" : "Afficher le menu"}
              aria-expanded={sidebarOpen}
            >
              <span className="hamburger" aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            </button>
            <div className="topbar-title">
              <p className="topbar-kicker">{meta.kicker}</p>
              <strong>{meta.title}</strong>
            </div>
          </div>

          <div className="topbar-right">
            {typeof indexedCount === "number" && (
              <span className="topbar-count">{indexedCount} documents</span>
            )}
            {isAdmin ? (
              <>
                <div className="topbar-user">
                  <span className="topbar-avatar" aria-hidden="true">
                    {initials(user?.name)}
                  </span>
                  <span className="topbar-user-text">
                    <strong>{user?.name}</strong>
                    <small>Administrateur</small>
                  </span>
                </div>
                <button type="button" className="btn ghost topbar-logout" onClick={logout}>
                  Déconnexion
                </button>
              </>
            ) : (
              <Link className="btn ghost topbar-logout" to="/connexion">
                Administration
              </Link>
            )}
          </div>
        </header>

        <div className="chrome-docks">
          <div className="back-dock">
            <BackButton fallback={isAdmin ? "/documents" : "/"} />
          </div>
          <div className="theme-dock">
            <ThemeSwitch />
          </div>
        </div>

        {error && (
          <div className="alert alert-error page-alert">
            <span>{error}</span>
            <button type="button" className="alert-dismiss" onClick={() => setError(null)}>
              Fermer
            </button>
          </div>
        )}

        <Outlet />
      </div>
    </div>
  );
}
