export default function EntityList({ entities }) {
  if (!entities || typeof entities !== "object" || Array.isArray(entities)) return null;

  const labels = {
    dates: "Dates",
    authors: "Auteurs",
    persons: "Personnes",
    organizations: "Organisations",
    locations: "Lieux",
    emails: "E-mails",
    phones: "Téléphones",
    keywords: "Mots-clés",
    domains: "Domaines",
  };

  const order = [
    "authors",
    "persons",
    "dates",
    "organizations",
    "locations",
    "keywords",
    "domains",
    "emails",
    "phones",
  ];

  const entries = order
    .filter((key) => Array.isArray(entities[key]) && entities[key].length > 0)
    .map((key) => [key, entities[key]]);

  // Clés inconnues éventuelles
  Object.entries(entities).forEach(([key, values]) => {
    if (order.includes(key)) return;
    if (Array.isArray(values) && values.length > 0) entries.push([key, values]);
  });

  if (entries.length === 0) return null;

  return (
    <div className="entities">
      <h4>Entités détectées</h4>
      <p className="entities-lead">
        Dates, auteurs, organisations et autres éléments extraits automatiquement du texte.
      </p>
      <div className="entities-grid">
        {entries.map(([key, values]) => (
          <div key={key} className="entity-item">
            <span className="entity-label">{labels[key] || key}</span>
            <div className="entity-chips">
              {values.map((value) => (
                <span key={`${key}-${value}`} className="entity-chip">
                  {value}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
