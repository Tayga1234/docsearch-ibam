# Figure 1. Pipeline d’indexation intelligente

À coller dans [Mermaid Live](https://mermaid.live) ou à prévisualiser dans Cursor, puis exporter en PNG pour le Word (`rapport/figures/fig1_pipeline.png`).

```mermaid
%%{init: {"flowchart": {"nodeSpacing": 36, "rankSpacing": 28, "padding": 12}}}%%
flowchart TB
  classDef etape fill:#E8EFF8,stroke:#1A365D,stroke-width:2px,color:#1A365D

  subgraph L1[" "]
    direction LR
    A["Fichiers<br/>PDF, DOCX, CSV, TXT"] --> B["Extraction<br/>du texte"]
  end

  subgraph L2[" "]
    direction LR
    C["Enrichissement<br/>tags, résumé, entités"] --> D["Stockage<br/>SQLite et Whoosh"]
  end

  subgraph L3[" "]
    direction LR
    E["Recherche<br/>mots-clés et hybride"] --> F["Interface<br/>web"]
  end

  B --> C
  D --> E

  class A,B,C,D,E,F etape
  style L1 fill:none,stroke:none
  style L2 fill:none,stroke:none
  style L3 fill:none,stroke:none
```
