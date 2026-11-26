import { useState } from "react";
import { Link } from "react-router-dom";
import ConfirmDialog from "../components/ConfirmDialog";
import Icon from "../components/Icon";
import { useApp } from "../context/AppContext";
import { rebuildIndex, scanDocuments, uploadDocument } from "../services/api";

function journalFromScan(data) {
  return {
    indexed: data.indexed || 0,
    skipped: data.skipped || 0,
    errors: data.errors || [],
    files: (data.errors || []).map((item) => ({
      name: item,
      status: "error",
      detail: item,
    })),
  };
}

export default function IngestPage() {
  const { apiStatus, refreshHealth, setError } = useApp();
  const [scanning, setScanning] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState("");
  const [rebuilding, setRebuilding] = useState(false);
  const [journal, setJournal] = useState(null);
  const [guard, setGuard] = useState(null);
  const pendingFiles = Array.isArray(guard) ? guard : null;
  const busy = scanning || uploading || rebuilding;
  const offline = !apiStatus;

  async function handleScan() {
    setScanning(true);
    setError(null);
    try {
      const data = await scanDocuments(true);
      setJournal(journalFromScan(data));
      await refreshHealth();
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  }

  async function runUpload(files) {
    if (!files?.length) return;
    setUploading(true);
    setError(null);
    const entries = [];
    let indexed = 0;
    let skipped = 0;
    const errors = [];
    try {
      for (let index = 0; index < files.length; index += 1) {
        const file = files[index];
        setUploadProgress(`${index + 1}/${files.length}`);
        try {
          const data = await uploadDocument(file);
          const status = data.status === "skipped" ? "skipped" : "indexed";
          if (status === "indexed") indexed += 1;
          else skipped += 1;
          entries.push({
            name: file.name,
            status,
            detail: data.document?.title || file.name,
          });
        } catch (err) {
          errors.push(`${file.name} : ${err.message}`);
          entries.push({ name: file.name, status: "error", detail: err.message });
        }
      }
      setJournal({ indexed, skipped, errors, files: entries });
      await refreshHealth();
    } finally {
      setUploading(false);
      setUploadProgress("");
    }
  }

  async function handleRebuild() {
    setRebuilding(true);
    setError(null);
    try {
      const data = await rebuildIndex();
      setJournal({ indexed: data.indexed, skipped: 0, errors: [], files: [] });
      await refreshHealth();
    } catch (err) {
      setError(err.message);
    } finally {
      setRebuilding(false);
    }
  }

  return (
    <section className="page page-ingest">
      <header className="page-intro">
        <p className="eyebrow">Administration</p>
        <h1>Indexation</h1>
        <p>
          {apiStatus?.documents ?? 0} document{(apiStatus?.documents || 0) > 1 ? "s" : ""} actuellement
          dans le fonds.
        </p>
      </header>

      <div className="action-grid">
        <article className="action-card">
          <span className="card-icon" aria-hidden="true">
            <Icon name="folder" size={22} />
          </span>
          <h2>Dossier local</h2>
          <p>Parcourt <code>data/raw</code> et indexe PDF, Word, CSV et TXT.</p>
          <button type="button" className="btn primary" onClick={() => setGuard("scan")} disabled={busy || offline}>
            <Icon name="folder" />
            {scanning ? "Indexation…" : "Indexer le dossier"}
          </button>
        </article>

        <article className="action-card">
          <span className="card-icon" aria-hidden="true">
            <Icon name="upload" size={22} />
          </span>
          <h2>Importer</h2>
          <p>Ajoute un ou plusieurs fichiers, puis les enrichit (tags, résumé, entités).</p>
          <label className={`btn ghost ${busy || offline ? "is-disabled" : ""}`}>
            <Icon name="upload" />
            {uploading ? `Envoi ${uploadProgress}…` : "Choisir des fichiers"}
            <input
              type="file"
              accept=".txt,.pdf,.docx,.csv"
              multiple
              onChange={(event) => {
                const files = Array.from(event.target.files || []);
                event.target.value = "";
                if (files.length) setGuard(files);
              }}
              disabled={busy || offline}
              hidden
            />
          </label>
        </article>

        <article className="action-card">
          <span className="card-icon" aria-hidden="true">
            <Icon name="rebuild" size={22} />
          </span>
          <h2>Reconstruire</h2>
          <p>Recrée l’index inversé à partir des documents déjà en base.</p>
          <button type="button" className="btn ghost" onClick={() => setGuard("rebuild")} disabled={busy || offline}>
            <Icon name="rebuild" />
            {rebuilding ? "Reconstruction…" : "Reconstruire l’index"}
          </button>
        </article>
      </div>

      {journal && (
        <div className="ingest-journal">
          <div className="journal-head">
            <span className="section-label">Journal d’indexation</span>
            <button type="button" className="alert-dismiss" onClick={() => setJournal(null)}>
              Fermer
            </button>
          </div>
          <p>
            Terminé — {journal.indexed} indexé(s)
            {journal.skipped ? `, ${journal.skipped} ignoré(s)` : ""}
            {journal.errors?.length ? `, ${journal.errors.length} erreur(s)` : ""}.
          </p>
          {journal.files?.length > 0 && (
            <ul className="journal-list">
              {journal.files.map((item, index) => (
                <li key={`${item.name}-${index}`}>
                  <span className={`journal-status is-${item.status === "indexed" ? "ok" : item.status === "skipped" ? "skip" : "err"}`}>
                    {item.status === "indexed" ? "Indexé" : item.status === "skipped" ? "Ignoré" : "Erreur"}
                  </span>
                  <strong>{item.name}</strong>
                  <span>{item.detail}</span>
                </li>
              ))}
            </ul>
          )}
          <Link to="/documents" className="alert-link">
            Voir les documents
          </Link>
        </div>
      )}

      <ConfirmDialog
        open={guard === "scan"}
        tone="warning"
        title="Indexer le dossier local ?"
        message="Le dossier data/raw sera parcouru et les fichiers déjà connus seront réindexés (force). Les documents absents du dossier ne sont pas supprimés."
        details={[`${apiStatus?.documents ?? 0} document(s) actuellement dans le fonds`]}
        confirmLabel="Lancer l’indexation"
        busy={scanning}
        onCancel={() => !scanning && setGuard(null)}
        onConfirm={async () => {
          await handleScan();
          setGuard(null);
        }}
      />

      <ConfirmDialog
        open={Boolean(pendingFiles)}
        tone="warning"
        title="Importer ces fichiers ?"
        message="Chaque fichier sera copié dans le fonds, enrichi puis indexé."
        details={(pendingFiles || []).slice(0, 8).map((file) => file.name)}
        confirmLabel={pendingFiles?.length > 1 ? `Importer ${pendingFiles.length} fichiers` : "Importer"}
        busy={uploading}
        onCancel={() => !uploading && setGuard(null)}
        onConfirm={async () => {
          await runUpload(pendingFiles);
          setGuard(null);
        }}
      />

      <ConfirmDialog
        open={guard === "rebuild"}
        tone="danger"
        title="Reconstruire l’index ?"
        message="L’index Whoosh sera recréé à partir des documents déjà en base. La recherche sera indisponible pendant l’opération. Les fichiers eux-mêmes ne sont pas effacés."
        details={[`${apiStatus?.documents ?? 0} document(s) à réindexer`]}
        confirmLabel="Reconstruire l’index"
        confirmWord="RECONSTRUIRE"
        busy={rebuilding}
        onCancel={() => !rebuilding && setGuard(null)}
        onConfirm={async () => {
          await handleRebuild();
          setGuard(null);
        }}
      />
    </section>
  );
}
