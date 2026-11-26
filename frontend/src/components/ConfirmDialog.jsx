import { useEffect, useId, useRef, useState } from "react";

export default function ConfirmDialog({
  open,
  tone = "warning",
  title,
  message,
  details = [],
  confirmLabel = "Confirmer",
  confirmWord = "",
  busy = false,
  onCancel,
  onConfirm,
}) {
  const titleId = useId();
  const inputRef = useRef(null);
  const [typed, setTyped] = useState("");
  const needsWord = Boolean(confirmWord);
  const wordOk = !needsWord || typed.trim() === confirmWord;
  const canSubmit = open && !busy && wordOk;

  useEffect(() => {
    if (!open) {
      setTyped("");
      return undefined;
    }
    const node = needsWord ? inputRef.current : null;
    node?.focus();

    function onKey(event) {
      if (event.key === "Escape" && !busy) {
        event.preventDefault();
        onCancel();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, busy, needsWord, onCancel]);

  if (!open) return null;

  function handleSubmit(event) {
    event.preventDefault();
    if (canSubmit) onConfirm();
  }

  return (
    <div className="confirm-backdrop" role="presentation" onClick={() => !busy && onCancel()}>
      <form
        className={`confirm-dialog is-${tone}`}
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={titleId}
        onClick={(event) => event.stopPropagation()}
        onSubmit={handleSubmit}
      >
        <p className="eyebrow">{tone === "danger" ? "Action irréversible" : "Confirmation requise"}</p>
        <h2 id={titleId}>{title}</h2>
        {message ? <p className="confirm-message">{message}</p> : null}
        {details.length > 0 && (
          <ul className="confirm-details">
            {details.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        )}
        {needsWord && (
          <label className="confirm-word">
            <span>
              Tapez <strong>{confirmWord}</strong> pour confirmer.
            </span>
            <input
              ref={inputRef}
              value={typed}
              onChange={(event) => setTyped(event.target.value)}
              autoComplete="off"
              spellCheck="false"
              disabled={busy}
              aria-label={`Saisir ${confirmWord} pour confirmer`}
            />
          </label>
        )}
        <div className="confirm-actions">
          <button type="button" className="btn ghost" onClick={onCancel} disabled={busy}>
            Annuler
          </button>
          <button type="submit" className={`btn ${tone === "danger" ? "danger" : "primary"}`} disabled={!canSubmit}>
            {busy ? "Traitement…" : confirmLabel}
          </button>
        </div>
      </form>
    </div>
  );
}
