import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import ThemeSwitch from "../components/ThemeSwitch";
import { clearSession } from "../services/api";
import { useAuth } from "../context/AuthContext";

const ADMIN_PROFILE = {
  username: "admin",
  password: "archives",
  role: "Administrateur",
  name: "Gaetan KOROGO",
  title: "Administrateur des archives",
  rights: "Indexer, importer, supprimer et reconstruire l’index. La consultation reste ouverte sans compte.",
};

export default function LoginPage() {
  const { user, isAdmin, login, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const redirectTo = location.state?.from?.pathname || "/indexation";

  if (user && isAdmin) {
    return <Navigate to={redirectTo} replace />;
  }

  async function submit(event, preset) {
    event?.preventDefault();
    const loginName = preset?.username || username;
    const loginPassword = preset?.password || password;
    setSubmitting(true);
    setError("");
    try {
      const nextUser = await login(loginName, loginPassword);
      if (nextUser?.role !== "admin") {
        await logout();
        clearSession();
        setError("Seul le compte administrateur peut ouvrir l’espace d’administration.");
        return;
      }
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="login-screen">
      <div className="login-top">
        <ThemeSwitch />
      </div>
      <section className="login-card">
        <div className="login-brand">
          <img src="/docusearch-logo.png" alt="" width={48} height={48} />
          <div>
            <p className="eyebrow">DocSearch · IBAM</p>
            <h1>Administration</h1>
          </div>
        </div>
        <p className="login-lead">
          La recherche et le fonds sont publics. Connectez-vous ici uniquement pour indexer,
          importer ou supprimer des documents.
        </p>

        <button
          type="button"
          className="profile-card"
          onClick={(event) => submit(event, ADMIN_PROFILE)}
          disabled={submitting}
        >
          <span className="eyebrow">{ADMIN_PROFILE.role}</span>
          <strong>{ADMIN_PROFILE.name}</strong>
          <span>{ADMIN_PROFILE.title}</span>
          <p>{ADMIN_PROFILE.rights}</p>
        </button>

        <details className="login-manual">
          <summary>Autre identifiant administrateur</summary>
          <form className="login-form" onSubmit={submit}>
            <label>
              Identifiant
              <input
                value={username}
                autoComplete="username"
                onChange={(event) => setUsername(event.target.value)}
              />
            </label>
            <label>
              Mot de passe
              <input
                type="password"
                value={password}
                autoComplete="current-password"
                onChange={(event) => setPassword(event.target.value)}
              />
            </label>
            <button type="submit" className="btn primary" disabled={submitting}>
              {submitting ? "Connexion…" : "Se connecter"}
            </button>
          </form>
        </details>
        {error && <p className="login-error">{error}</p>}
        <p className="login-lead" style={{ marginTop: "1rem" }}>
          <Link to="/">Retour à l’espace public</Link>
        </p>
      </section>
    </div>
  );
}
