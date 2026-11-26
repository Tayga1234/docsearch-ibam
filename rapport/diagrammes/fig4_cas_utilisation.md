# Figure 4. Diagramme de cas d’utilisation de DocSearch

Coller le bloc ci-dessous (sans les trois backticks) dans [Mermaid Live](https://mermaid.live).

```
%%{init: {"flowchart": {"nodeSpacing": 18, "rankSpacing": 32, "padding": 8}}}%%
flowchart LR
  classDef cas fill:#E8EFF8,stroke:#1A365D,stroke-width:1.5px,color:#1A365D

  L@{ shape: actor, label: "Lecteur" }

  subgraph CONS[Consultation]
    AUTH((Se connecter))
    REC((Rechercher))
    FIC((Consulter fiche))
    FON((Parcourir fonds))
    CMP((Comparer modes))
    EXP((Exporter fiche))
  end

  subgraph ADM[Administration]
    SCA((Scanner dossier))
    UPL((Televerser))
    IDX((Indexer et enrichir))
    SUP((Supprimer))
    REB((Reconstruire index))
  end

  A@{ shape: actor, label: "Administrateur" }

  L --- AUTH
  L --- REC
  L --- FIC
  L --- FON
  A --- SCA
  A --- UPL
  A --- SUP
  A --- REB
  CMP -.->|extend| REC
  EXP -.->|extend| FIC
  SCA -.->|include| IDX
  UPL -.->|include| IDX
  A -.->|heritage| L

  class AUTH,REC,FIC,FON,CMP,EXP,SCA,UPL,IDX,SUP,REB cas
```
