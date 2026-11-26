export default function EmptyState({ icon = "∅", title, children }) {
  return (
    <div className="empty-state">
      {icon === "spinner" ? <div className="spinner" /> : <div className="empty-icon">{icon}</div>}
      {title && <h4>{title}</h4>}
      {children}
    </div>
  );
}
