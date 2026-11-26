"""Cadre institutionnel réel, personnes et montants fictifs du prototype."""

from pathlib import Path

ETABLISSEMENT = "Institut Burkinabè des Arts et Métiers"
SIGLE = "IBAM"
UNIVERSITE = "Université Joseph Ki-Zerbo"
SIGLE_UNIV = "UJKZ"
MINISTERE = (
    "Ministère de l'Enseignement supérieur, de la Recherche et de l'Innovation"
)
DEVISE = "Unité – Progrès – Justice"
BP = "03 BP 7021 Ouagadougou 03"
TEL = "(+226) 25 30 70 64 / 65"
FAX = "(+226) 25 30 72 42"
CAMPUS = "Campus de Ouagadougou, secteur 25 — antenne pédagogique de Somgandé"
SITE = "https://www.ujkz.bf/ibam/"

SERVICES = {
    "direction": "Direction de l'IBAM",
    "scolarite": "Service de la scolarité et des examens",
    "rh": "Service des ressources humaines",
    "agence": "Agence comptable de l'IBAM",
    "dsi": "Service des systèmes d'information",
    "doc": "Centre de documentation et des archives",
    "stages": "Cellule des stages et de l'insertion professionnelle",
    "st": "Département Sciences et Technologie",
    "seg": "Département Sciences économiques et de gestion",
    "qualite": "Cellule qualité et évaluation",
}

PERSONNES = {
    "fatou": "Fatou Sanou, documentaliste",
    "ibrahim": "Ibrahim Ouédraogo, chef du service des systèmes d'information",
    "aminata": "Aminata Kaboré, cheffe du service de la scolarité",
    "mariam": "Mariam Traoré, cheffe du service des ressources humaines",
    "boureima": "Boureima Sawadogo, agent comptable",
    "claire": "Claire Nikièma, assistante de direction",
    "adama": "Adama Ouédraogo, chef du département Sciences et Technologie",
    "salimata": "Salimata Zongo, cheffe du département Sciences économiques et de gestion",
    "moussa": "Moussa Compaoré, responsable des stages",
    "david": "David Kaboré, archiviste",
    "gaetan": "Gaëtan KOROGO, stagiaire Master MISIE / administrateur DocSearch",
    "rasmane": "Rasmané Ilboudo, enseignant MIAGE",
    "awa": "Awa Ouédraogo, enseignante CCA",
    "paulin": "Paulin Yaméogo, responsable qualité",
}

FILIERES = [
    "Comptabilité-Contrôle-Audit (CCA)",
    "Assurance-Banque-Finance (ABF)",
    "Marketing et Gestion (MG)",
    "Assistant de Direction Bilingue (ADB)",
    "Méthodes Informatiques Appliquées à la Gestion (MIAGE)",
    "Master MISIE — Ingénierie des systèmes d'information en entreprise",
    "Master Administration et Gestion des Entreprises (AGE)",
    "Master Comptabilité-Contrôle-Audit",
    "Master Banque et Finance",
    "Master Sciences de Gestion",
]

MAIL = {
    "direction": "direction.ibam@ujkz.bf",
    "scolarite": "scolarite.ibam@ujkz.bf",
    "rh": "rh.ibam@ujkz.bf",
    "agence": "agence.comptable.ibam@ujkz.bf",
    "dsi": "dsi.ibam@ujkz.bf",
    "doc": "documentation.ibam@ujkz.bf",
    "stages": "stages.ibam@ujkz.bf",
}

FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
