export default function StatusBadge({ apiStatus, loading }) {
  return (
    <div className={`status-pill ${apiStatus ? "online" : "offline"}`}>
      <span className="status-dot" />
      {loading
        ? "Connexion..."
        : apiStatus
          ? `API v${apiStatus.version}`
          : "API hors ligne"}
    </div>
  );
}
