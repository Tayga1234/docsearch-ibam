import { useNavigate } from "react-router-dom";

export default function BackButton({ fallback = "/" }) {
  const navigate = useNavigate();

  function goBack() {
    if (window.history.length > 1) {
      navigate(-1);
      return;
    }
    navigate(fallback);
  }

  return (
    <button type="button" className="back-fab" onClick={goBack} aria-label="Retour" title="Retour">
      <svg className="back-fab-icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
        <path
          d="M14.5 5.5 7 12l7.5 6.5"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  );
}
