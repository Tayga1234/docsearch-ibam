# Travaux — Revue de littérature

**Thème :** Indexation intelligente de données pour la recherche d'information  

**État de l’art du rapport (chapitre complet) :** [`../rapport/02_etat_de_lart.md`](../rapport/02_etat_de_lart.md) — moteurs avec/sans index + 15 articles.  
**Période :** 2022–2026  
**Corpus :** 15 articles — 5 articles par jour, 3 jours

---

## Méthode de travail

### a. Lecture quotidienne

| Jour | Fichier | Articles | Orientation |
|------|---------|----------|-------------|
| Jour 1 | [JOUR_1.md](JOUR_1.md) | 1 à 5 | Fondements, données semi-structurées, GenIR |
| Jour 2 | [JOUR_2.md](JOUR_2.md) | 6 à 10 | Recherche générative, hybridation, graphes |
| Jour 3 | [JOUR_3.md](JOUR_3.md) | 11 à 15 | Ingestion, vision, chunking, métadonnées |

Pour chaque article :
- intitulé ;
- résumé personnel (~200 mots), distinct de l'abstract ;
- citation des auteurs dans le résumé.

### b. à e. Synthèse du travail

| Section | Fichier |
|---------|---------|
| b. Résumé général (< 1000 mots) | [A_resume_general.md](A_resume_general.md) |
| c. Introduction générale | [B_introduction_generale.md](B_introduction_generale.md) |
| d. Corps du travail | [C_corps_du_travail.md](C_corps_du_travail.md) |
| e. Conclusion et perspectives | [D_conclusion_perspectives.md](D_conclusion_perspectives.md) |

### Document Word fusionné

```powershell
.venv\Scripts\python.exe scripts\export_travaux_word.py
```

Fichier principal : `word/TRAVAIL_COMPLET.docx`

### Présentation du projet tutoré

| Fichier | Usage |
|---------|--------|
| [PRESENTATION_PROJET_TUTORE.pptx](PRESENTATION_PROJET_TUTORE.pptx) | Slides de présentation (10) |
| [NOTES_ORATEUR_PROJET_TUTORE.md](NOTES_ORATEUR_PROJET_TUTORE.md) | Notes orateur + questions jury |

### Présentation validation du thème (jury)

```powershell
.venv\Scripts\python.exe scripts\gen_presentation_theme.py
```

| Fichier | Usage |
|---------|--------|
| [PRESENTATION_VALIDATION_THEME.pptx](PRESENTATION_VALIDATION_THEME.pptx) | Slides pour convaincre le jury |
| [NOTES_ORATEUR_VALIDATION_THEME.md](NOTES_ORATEUR_VALIDATION_THEME.md) | Texte à dire + questions probables |
