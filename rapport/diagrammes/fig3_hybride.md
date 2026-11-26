# Figure 3. Fusion des scores en recherche hybride

Coller le bloc ci-dessous (sans les trois backticks) dans [Mermaid Live](https://mermaid.live).

```
flowchart TB
  classDef etape fill:#E8EFF8,stroke:#1A365D,stroke-width:2px,color:#1A365D
  classDef resultat fill:#2F6FB0,stroke:#1A365D,stroke-width:2px,color:#FFFFFF
  classDef note fill:#FFFFFF,stroke:#1A365D,stroke-width:1px,color:#1A365D

  Q["Requête utilisateur"] --> L["Whoosh<br/>mots-clés · poids 0,6"]
  Q --> S["TF-IDF<br/>similarité · poids 0,4"]
  L --> N["Normalisation<br/>par le score max de chaque liste"]
  S --> N
  N --> C["Score combiné<br/>0,6 × lexical + 0,4 × sémantique<br/>liste classée"]

  C -.- NOTE["Extrait lexical conservé en priorité<br/>surbrillance. Mode par défaut : hybride."]

  class Q,L,S,N etape
  class C resultat
  class NOTE note
```
