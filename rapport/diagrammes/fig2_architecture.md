# Figure 2. Architecture logique de DocSearch

À coller dans [Mermaid Live](https://mermaid.live) ou à prévisualiser dans Cursor, puis exporter en PNG pour le Word (`rapport/figures/fig2_architecture.png`).

Le client n’accède jamais directement à l’index : toute requête passe par l’API.

```mermaid
flowchart TB
  classDef couche fill:#E8EFF8,stroke:#1A365D,stroke-width:2px,color:#1A365D
  classDef stock fill:#FFFFFF,stroke:#1A365D,stroke-width:1px,color:#1A365D

  subgraph P["Présentation"]
    UI["Interface React<br/>recherche · résultats · fiche · téléversement"]
  end

  subgraph A["API REST"]
    API["FastAPI<br/>validation Pydantic · documentation OpenAPI"]
  end

  subgraph M["Métier"]
    MET["ingestion · extraction · enrichissement · indexation · recherche"]
  end

  subgraph S["Stockage"]
    RAW["Fichiers bruts<br/>data/raw/"]
    SQL["SQLite<br/>métadonnées · texte · tags"]
    WHO["Index Whoosh<br/>recherche lexicale"]
  end

  UI --> API
  API --> MET
  MET --> RAW
  MET --> SQL
  MET --> WHO

  class UI,API,MET couche
  class RAW,SQL,WHO stock
```
