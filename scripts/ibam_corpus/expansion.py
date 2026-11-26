"""
Fonds étendu IBAM / UJKZ — reconstitutions pédagogiques 2020-2026.

Les 900 pièces supplémentaires simulent le rythme réel d'un centre de
documentation universitaire : notes, PV, circulaires, registres, listes,
devis et rapports. Cadre institutionnel réel ; personnes et montants fictifs.
La génération est déterministe (graine fixe) pour rester reproductible.
"""

from __future__ import annotations

import random

from .identite import FILIERES, MAIL, PERSONNES, SERVICES
from .modele import Piece

SEED = 20251104
CIBLE = 1010

MOIS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]

NOMS = [
    "Ouédraogo",
    "Kaboré",
    "Sawadogo",
    "Traoré",
    "Zongo",
    "Compaoré",
    "Nikièma",
    "Ilboudo",
    "Yaméogo",
    "Bationo",
    "Somé",
    "Dabiré",
    "Guigma",
    "Ouattara",
    "Sanou",
    "Tapsoba",
    "Lingani",
    "Kinda",
    "Zida",
    "Nacanabo",
    "Bonkoungou",
    "Ganemtoré",
    "Kientega",
    "Ouédraogo",
    "Savadogo",
]

PRENOMS = [
    "Fatou",
    "Aminata",
    "Mariam",
    "Salimata",
    "Awa",
    "Claire",
    "Aïcha",
    "Nadia",
    "Inès",
    "Estelle",
    "Ibrahim",
    "Moussa",
    "Adama",
    "Issa",
    "Salif",
    "Karim",
    "Issouf",
    "Hassane",
    "Yacouba",
    "Paulin",
    "David",
    "Rasmané",
    "Boukary",
    "Abdoulaye",
    "Wendyam",
]

SERVICES_LIST = list(SERVICES.items())
SIGNATAIRES = list(PERSONNES.values())

PARTENAIRES = [
    "Chambre de commerce et d'industrie du Burkina Faso",
    "ANPTIC",
    "Université Nazi Boni",
    "Université Norbert Zongo",
    "CAMES",
    "SONABEL",
    "ONEA",
    "Ministère de l'Enseignement supérieur, de la Recherche et de l'Innovation",
    "Présidence de l'Université Joseph Ki-Zerbo",
    "Direction générale des impôts",
    "Trésor public",
    "cabinet d'expertise comptable SAWADOGO & Associés",
    "Banque agricole du Faso",
    "Office national des télécommunications",
]

LIEUX = [
    "campus principal, secteur 25",
    "complexe pédagogique de Somgandé",
    "salle de lecture du Centre de documentation",
    "magasin A des archives",
    "magasin B (examens)",
    "salle multimédia",
    "local technique DSI",
    "amphithéâtre A",
    "salle conseil de l'institut",
    "laboratoire MIAGE",
]

PROCESSUS = [
    "versement d'archives",
    "inscription administrative CampusFaso",
    "liquidation de facture",
    "organisation des examens",
    "prêt d'ouvrages",
    "sauvegarde du serveur DocSearch",
    "évaluation des enseignements",
    "accueil des stagiaires",
    "contrôle d'accès visiteur",
    "numérisation des PV",
]

INCIDENTS = [
    ("coupure SONABEL", "Le local technique a basculé sur onduleur pendant 47 minutes. Les postes de la salle de lecture sont restés hors ligne."),
    ("fuite climatisation magasin A", "David Kaboré a isolé les cartons du rayon E2. Un devis Froid-Services est demandé."),
    ("perte de lien fibre", "La DSI a basculé temporairement sur le lien secondaire. DocSearch est resté accessible en local."),
    ("incident badge visiteur", "Deux badges n'ont pas été restitués après la visite MESRSI. La procédure d'accueil est rappelée."),
    ("erreur d'affichage de résultats", "Une liste partielle a été collée à Somgandé. La scolarité a publié un rectificatif le lendemain."),
    ("retard de versement scolarité", "Dix-huit pièces de session de janvier n'étaient pas au magasin B à J+10. Rappel de la procédure 2.1."),
    ("ticket DSI non clos", "Le ticket T-réseau-Somgandé est ouvert depuis onze jours. Relance Ibrahim Ouédraogo."),
    ("ouvrage non restitué", "Trois monographies CCA dépassent 21 jours. Relance aux emprunteurs via la scolarité."),
]

SESSIONS = ["janvier", "juin", "septembre", "rattrapage d'octobre"]
NIVEAUX = ["L1", "L2", "L3", "M1", "M2"]
REGIMES = ["jour", "soir"]


def _date(rng: random.Random, annee: int | None = None) -> tuple[str, int, int]:
    annee = annee if annee is not None else rng.randint(2020, 2026)
    mois = rng.randint(1, 12)
    jour = rng.randint(1, 28)
    return f"{jour} {MOIS[mois - 1]} {annee}", annee, mois


def _personne(rng: random.Random) -> tuple[str, str]:
    return rng.choice(NOMS), rng.choice(PRENOMS)


def _email(prenom: str, nom: str, etudiant: bool = False) -> str:
    base = f"{prenom.lower()}.{nom.lower()}".replace(" ", "").replace("'", "")
    base = (
        base.replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("ë", "e")
        .replace("à", "a")
        .replace("ï", "i")
        .replace("ô", "o")
        .replace("ù", "u")
        .replace("ç", "c")
    )
    domaine = "etudiant.ujkz.bf" if etudiant else "ujkz.bf"
    return f"{base}@{domaine}"


def _service(rng: random.Random) -> tuple[str, str]:
    return rng.choice(SERVICES_LIST)


def _montant(rng: random.Random, mini: int = 25_000, maxi: int = 4_800_000) -> str:
    valeur = rng.randrange(mini, maxi, 5_000)
    return f"{valeur:,}".replace(",", " ") + " FCFA"


def _filiere(rng: random.Random) -> str:
    return rng.choice(FILIERES)


def _signataire(rng: random.Random) -> str:
    return rng.choice(SIGNATAIRES)


def _ref(code: str, typ: str, annee: int, n: int) -> str:
    return f"IBAM/{code}/{typ}/{annee}/{n:04d}"


def _intro(service: str, annee: int, piece_type: str) -> str:
    return (
        f"Le {service} de l'Institut Burkinabè des Arts et Métiers, établissement de "
        f"l'Université Joseph Ki-Zerbo (03 BP 7021 Ouagadougou 03), établit la présente "
        f"{piece_type} au titre de l'année {annee}. La pièce est destinée au fonds interne "
        f"du Centre de documentation et des archives. Elle sera indexée dans DocSearch "
        f"dans les quarante-huit heures suivant la signature, conformément à la procédure "
        f"d'archivage numérique."
    )


def _cloture(annee: int, lieu: str) -> str:
    return (
        f"La présente pièce est exécutoire pour les services concernés. Ampliations : "
        f"Direction de l'IBAM, Centre de documentation, chrono {annee}. Lieu d'application : "
        f"{lieu}. Devise : Unité – Progrès – Justice."
    )


def notes_de_service(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    sujets = [
        (
            "formation",
            "Plan de formation interne — {mois} {annee}",
            "Une session de {duree} jour(s) est organisée à {lieu} pour le personnel de {service}. "
            "Le thème porte sur {processus}. La présence est obligatoire pour les secrétariats concernés. "
            "Fatou Sanou et Mariam Traoré coordonnent l'émargement.",
            "Les supports seront versés au portail DocSearch sous cote FORM-{annee}. "
            "Aucun frais n'est demandé aux agents. Une attestation interne sera délivrée.",
        ),
        (
            "budget",
            "Point d'exécution budgétaire — {trimestre} {annee}",
            "L'agence comptable dresse le point de la ligne documentaire et des imputations de {service}. "
            "Le reliquat disponible s'élève à {montant}. Toute dépense supérieure à 150 000 FCFA "
            "requiert trois devis, comme le rappelle Boureima Sawadogo.",
            "Les liquidations en souffrance doivent parvenir avant le 25 du mois. "
            "Les pièces justificatives originales restent au magasin comptable ; une copie PDF texte "
            "est versée aux archives.",
        ),
        (
            "archives",
            "Campagne de versement — {service} — {mois} {annee}",
            "David Kaboré ouvre une campagne de versement pour les dossiers clos de {service}. "
            "Sont attendus : notes signées, PV, listes anonymisées, conventions. "
            "Les dossiers nominatifs RH et les copies d'examen restent hors périmètre DocSearch.",
            "Délai : dix jours ouvrés. Bordereau obligatoire. Les PDF image sans couche texte "
            "seront refusés jusqu'à OCR, conformément à l'alerte qualité.",
        ),
        (
            "examens",
            "Organisation de la session {session} {annee}",
            "Aminata Kaboré fixe le calendrier de la session {session} {annee} pour {_filiere}. "
            "Les salles de {lieu} sont réservées. Convocation CampusFaso et affichage papier.",
            "Surveillance : un enseignant titulaire plus un vacataire par salle de plus de quarante "
            "candidats. Les copies sont conservées deux ans au magasin B. Réclamations : cinq jours ouvrés.",
        ),
        (
            "reseau",
            "Maintenance du réseau et du serveur documentaire — {mois} {annee}",
            "Ibrahim Ouédraogo programme une fenêtre de maintenance à {lieu}. "
            "DocSearch pourra être indisponible de 18 h 00 à 20 h 30. Les postes de scolarité "
            "basculent sur le partage local.",
            "Un test de restauration est prévu le lundi suivant. Compte rendu versé sous cote DSI-SAV-{annee}.",
        ),
        (
            "qualite",
            "Revue de processus — {processus}",
            "Paulin Yaméogo convoque la revue trimestrielle du processus « {processus} ». "
            "Indicateurs : délai, taux de pièces incomplètes, incidents répétés.",
            "Les non-conformités ouvertes depuis plus de trente jours sont présentées au conseil. "
            "Les actions correctives sont indexées sous cote QUAL-AC.",
        ),
        (
            "stages",
            "Campagne de stages {annee} — {_filiere}",
            "Moussa Compaoré ouvre la campagne de stages pour {_filiere}, régime {regime}. "
            "Les conventions types sont disponibles au Centre de documentation et dans DocSearch. "
            "Partenaire pressenti : {partenaire}.",
            "Date limite de dépôt des sujets : quinze jours avant le départ. "
            "Les rapports non confidentiels sont versés au fonds dans les quinze jours suivant la soutenance.",
        ),
        (
            "documentation",
            "Fonctionnement du Centre de documentation — {mois} {annee}",
            "Fatou Sanou rappelle les horaires et les règles de prêt à {lieu}. "
            "Les mémoires sous embargo ne circulent pas. Les enseignants signalent les lacunes d'acquisition "
            "avant la fin du mois.",
            "Les statistiques de prêts du mois précédent sont jointes au registre CSV. "
            "Toute reproduction de délibération est interdite sans visa de la Direction.",
        ),
        (
            "rh",
            "Congés, astreintes et remplacement — {mois} {annee}",
            "Le service des ressources humaines publie le tableau des congés de {service}. "
            "Les astreintes documentation du samedi matin restent assurées par rotation.",
            "Les demandes tardives ne sont plus acceptées après le 20 du mois précédent, "
            "sauf cas de force majeure visé par Mariam Traoré.",
        ),
        (
            "pedagogie",
            "Ajustement de maquette — {_filiere} {annee}",
            "Le département concerné propose un ajustement de la maquette {_filiere} pour {annee}. "
            "L'ajustement porte sur le volume horaire, les projets tutorés et l'évaluation LMD.",
            "Avis demandé au conseil pédagogique. Une fois adopté, le document de maquette "
            "est versé au fonds et signalé aux délégués d'étudiants.",
        ),
        (
            "securite",
            "Exercice de sécurité incendie — {lieu}",
            "Un exercice d'évacuation est programmé à {lieu}. Le personnel et les lecteurs "
            "suivent le chemin balisé vers le point de rassemblement du parking nord.",
            "Les extincteurs du magasin A ont été contrôlés. Un compte rendu est adressé à la Direction "
            "et versé aux archives sous cote SEC-{annee}.",
        ),
        (
            "partenariat",
            "Accueil d'une délégation — {partenaire}",
            "La Direction de l'IBAM accueille une délégation de {partenaire} à {lieu}. "
            "Programme : présentation des filières, visite du Centre de documentation, "
            "démonstration facultative de DocSearch en lecture seule.",
            "Claire Nikièma assure le protocole. Les badges visiteurs sont restitués le jour même. "
            "Un compte rendu de visite est versé sous dix jours.",
        ),
    ]

    for i in range(n):
        key, service = _service(rng)
        date, annee, mois = _date(rng)
        code_sujet, titre, p1, p2 = sujets[i % len(sujets)]
        contexte = {
            "mois": MOIS[mois - 1],
            "annee": annee,
            "service": service,
            "lieu": rng.choice(LIEUX),
            "processus": rng.choice(PROCESSUS),
            "montant": _montant(rng),
            "trimestre": f"T{((mois - 1) // 3) + 1}",
            "session": rng.choice(SESSIONS),
            "_filiere": _filiere(rng),
            "regime": rng.choice(REGIMES),
            "partenaire": rng.choice(PARTENAIRES),
            "duree": rng.choice([1, 2, 3]),
        }
        pieces.append(
            Piece(
                nom=f"note_{key}_{annee}_{i:04d}.txt",
                service=service,
                ref=_ref(key[:3].upper(), "NS", annee, i + 1),
                date=date,
                objet=titre.format(**contexte),
                signataire=_signataire(rng),
                destinataires=f"{service}, Centre de documentation",
                paragraphes=[
                    _intro(service, annee, "note de service"),
                    p1.format(**contexte),
                    p2.format(**contexte),
                    (
                        f"Référence interne : dossier {key}-{annee}-{i:04d}. "
                        f"Contact : {MAIL.get(key if key in MAIL else 'doc', MAIL['doc'])}. "
                        f"Cette note ne se substitue pas au règlement intérieur ni aux décisions du conseil."
                    ),
                    _cloture(annee, contexte["lieu"]),
                ],
            )
        )
    return pieces


def convocations(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    motifs = [
        "conseil de l'institut",
        "conseil pédagogique",
        "réunion des correspondants versants",
        "cellule qualité",
        "comité de suivi DocSearch",
        "préparation de la session d'examens",
        "comité budget documentation",
        "réunion des délégués d'étudiants",
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        motif = motifs[i % len(motifs)]
        lieu = rng.choice(LIEUX)
        heure = rng.choice(["8 h 30", "10 h 00", "14 h 30", "16 h 00", "18 h 15"])
        pieces.append(
            Piece(
                nom=f"convocation_{annee}_{i:04d}.txt",
                service=SERVICES["direction"],
                ref=_ref("DIR", "CONV", annee, i + 1),
                date=date,
                objet=f"Convocation — {motif} du {date}",
                signataire=PERSONNES["claire"],
                destinataires="Membres convoqués, archives",
                paragraphes=[
                    _intro(SERVICES["direction"], annee, "convocation"),
                    (
                        f"Les membres sont convoqués le {date} à {heure}, {lieu}, pour {motif}. "
                        f"L'ordre du jour comprend : (1) adoption du compte rendu précédent ; "
                        f"(2) point d'étape du service concerné ; (3) questions diverses. "
                        f"Les pièces de séance seront déposées la veille au Centre de documentation."
                    ),
                    (
                        f"En cas d'empêchement, un suppléant dûment mandaté peut siéger. "
                        f"La feuille d'émargement sera versée au fonds. "
                        f"Un extrait des décisions sera indexé dans DocSearch, hors mentions nominatives."
                    ),
                    _cloture(annee, lieu),
                ],
            )
        )
    return pieces


def comptes_rendus_incidents(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    for i in range(n):
        date, annee, mois = _date(rng)
        titre, detail = INCIDENTS[i % len(INCIDENTS)]
        key, service = _service(rng)
        pieces.append(
            Piece(
                nom=f"incident_{annee}_{i:04d}.txt",
                service=service,
                ref=_ref("DSI" if "réseau" in titre or "SONABEL" in titre else "DIR", "INC", annee, i + 1),
                date=date,
                objet=f"Compte rendu d'incident — {titre}",
                signataire=_signataire(rng),
                destinataires="Direction, DSI, documentation, qualité",
                paragraphes=[
                    _intro(service, annee, "compte rendu d'incident"),
                    (
                        f"Le {date}, un incident a été constaté : {titre}. {detail} "
                        f"Lieu : {rng.choice(LIEUX)}. Témoins : {_personne(rng)[1]} {_personne(rng)[0]} "
                        f"et l'agent de permanence."
                    ),
                    (
                        f"Mesures immédiates : sécurisation des personnes et des fonds documentaires, "
                        f"information de {PERSONNES['ibrahim']} et de {PERSONNES['fatou']}. "
                        f"Impact sur DocSearch : {'indisponibilité partielle' if i % 3 == 0 else 'aucun'}. "
                        f"Coût estimé des réparations : {_montant(rng, 15_000, 650_000)}."
                    ),
                    (
                        "Recommandations : mettre à jour la procédure concernée, former le personnel "
                        "de permanence, verser ce compte rendu sous cote INC. "
                        "Paulin Yaméogo inscrit l'événement au registre qualité."
                    ),
                    _cloture(annee, rng.choice(LIEUX)),
                ],
            )
        )
    return pieces


def procedures(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    titres = [
        "Procédure de versement numérique",
        "Procédure de prêt entre bibliothèques",
        "Procédure d'inscription et de confirmation physique",
        "Procédure de liquidation des factures documentaires",
        "Procédure de sauvegarde et de restauration",
        "Procédure d'accueil des visiteurs",
        "Procédure de réclamation de notes",
        "Procédure de numérisation des PV",
        "Procédure de gestion des badges",
        "Procédure de clôture annuelle des archives",
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        titre = titres[i % len(titres)]
        version = f"{1 + (i // len(titres))}.{1 + (i % 5)}"
        key, service = _service(rng)
        pieces.append(
            Piece(
                nom=f"procedure_{annee}_{i:04d}.txt",
                service=service,
                ref=_ref("QUA", "PRO", annee, i + 1),
                date=date,
                objet=f"{titre} — version {version}",
                signataire=PERSONNES["paulin"],
                destinataires="Tous services",
                paragraphes=[
                    _intro(service, annee, "procédure"),
                    f"## 1. Objet et champ",
                    (
                        f"La présente procédure version {version} décrit {titre.lower()} au sein de l'IBAM. "
                        f"Elle s'applique au campus principal et à Somgandé. Elle remplace toute version antérieure "
                        f"non homologuée par la cellule qualité."
                    ),
                    "## 2. Rôles",
                    (
                        f"Pilote : {service}. Contributeurs : Centre de documentation, DSI, scolarité selon le cas. "
                        f"Le correspondant versant de chaque service applique les délais. "
                        f"Fatou Sanou refuse les pièces hors nomenclature."
                    ),
                    "## 3. Déroulement",
                    (
                        "Préparer la pièce (PDF texte, DOCX ou CSV selon le type) ; renseigner le bordereau ; "
                        "déposer dans le répertoire de versement ; contrôler l'indexation dans DocSearch ; "
                        "archiver le bordereau signé. Délai cible : quarante-huit heures après signature."
                    ),
                    "## 4. Enregistrements",
                    (
                        f"Les enregistrements sont conservés {3 + (i % 4)} ans au magasin A, hors copies d'examen "
                        f"(magasin B, deux ans). Toute dérogation est visée par la Direction."
                    ),
                    _cloture(annee, rng.choice(LIEUX)),
                ],
            )
        )
    return pieces


def faq_thematiques(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    themes = [
        (
            "prêt d'ouvrages",
            "La durée de prêt est de 14 jours, renouvelable une fois si l'ouvrage n'est pas réservé. "
            "Les mémoires sous embargo et les délibérations ne se prêtent pas.",
        ),
        (
            "accès DocSearch",
            "Le portail n'est joignable que depuis le réseau campus. Profil lecteur : recherche et consultation. "
            "Profil administrateur : versement, suppression, reconstruction d'index.",
        ),
        (
            "attestation de scolarité",
            "Le modèle unique est délivré par la scolarité sur présentation de la quittance. "
            "Délai affiché : 72 heures hors pic de rentrée.",
        ),
        (
            "convention de stage",
            "Trois signatures sont exigées (IBAM, étudiant, organisme). Sans visa de Moussa Compaoré, "
            "le stage n'est pas pédagogique.",
        ),
        (
            "réclamation de notes",
            "Écrit, cinq jours ouvrés, auprès d'Aminata Kaboré. Pas de contestation orale en salle.",
        ),
        (
            "horaires de la documentation",
            "Lundi–vendredi 7 h 30–17 h 30 ; samedi 8 h 00–12 h 30 hors vacances. "
            "Fermeture exceptionnelle affichée 48 h à l'avance.",
        ),
        (
            "dons d'ouvrages",
            "Acceptés s'ils sont complets, non annotés et pertinents pour CCA, MIAGE, MISIE, ABF, MG ou ADB. "
            "Les doubles sont cédés ou pilonnés selon l'état.",
        ),
        (
            "confidentialité",
            "Les listes nominatives d'examens et les dossiers RH ne sont pas indexés. "
            "Toute extraction hors réseau est soumise à la Direction.",
        ),
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        theme, reponse = themes[i % len(themes)]
        pieces.append(
            Piece(
                nom=f"faq_{annee}_{i:04d}.txt",
                service=SERVICES["doc"],
                ref=_ref("DOC", "FAQ", annee, i + 1),
                date=date,
                objet=f"FAQ du Centre de documentation — {theme}",
                signataire=PERSONNES["fatou"],
                destinataires="Usagers, secrétariats",
                paragraphes=[
                    _intro(SERVICES["doc"], annee, "fiche FAQ"),
                    f"Question fréquente : {theme}.",
                    reponse,
                    (
                        "Cette fiche complète le règlement intérieur et le guide DocSearch. "
                        "Elle ne crée pas de droit nouveau. Pour un cas particulier, s'adresser à l'accueil "
                        "documentation ou ouvrir un ticket DSI si l'outil est en cause."
                    ),
                    _cloture(annee, "salle de lecture du Centre de documentation"),
                ],
            )
        )
    return pieces


def proces_verbaux(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    instances = [
        ("conseil de l'institut", "DIR", SERVICES["direction"]),
        ("conseil pédagogique", "SCOL", SERVICES["scolarite"]),
        ("cellule qualité", "QUA", SERVICES["qualite"]),
        ("comité DSI", "DSI", SERVICES["dsi"]),
        ("comité documentation", "DOC", SERVICES["doc"]),
        ("réunion des stages", "STG", SERVICES["stages"]),
        ("assemblée département ST", "ST", SERVICES["st"]),
        ("assemblée département SEG", "SEG", SERVICES["seg"]),
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        instance, code, service = instances[i % len(instances)]
        filiere = _filiere(rng)
        montant = _montant(rng, 80_000, 2_500_000)
        pieces.append(
            Piece(
                nom=f"pv_{code.lower()}_{annee}_{i:04d}.docx",
                service=service,
                ref=_ref(code, "PV", annee, i + 1),
                date=date,
                objet=f"Procès-verbal — {instance} du {date}",
                signataire=_signataire(rng),
                destinataires="Membres, archives",
                paragraphes=[
                    "## Présents et ordre du jour",
                    _intro(service, annee, "procès-verbal"),
                    (
                        f"L'{instance} s'est réuni(e) à {rng.choice(LIEUX)}. "
                        f"Présidence de séance : { _signataire(rng) }. "
                        f"Secrétariat de séance : {PERSONNES['claire'] if i % 2 == 0 else PERSONNES['david']}. "
                        f"Ordre du jour : situation de {filiere} ; {rng.choice(PROCESSUS)} ; budget ({montant})."
                    ),
                    "## Délibérations",
                    (
                        f"Après débat, l'instance prend acte du rapport oral et décide : "
                        f"(1) de poursuivre le plan d'actions {annee} ; "
                        f"(2) de verser les pièces adoptées au Centre de documentation ; "
                        f"(3) de charger le service pilote d'un compte rendu à J+15. "
                        f"Vote : adopté à la majorité des présents."
                    ),
                    "## Documentation et suivi",
                    (
                        "Les annexes (listes d'émargement, extraits budgétaires, maquettes) sont jointes au dossier "
                        "papier et, lorsqu'elles sont communicables, indexées dans DocSearch. "
                        "Les mentions nominatives d'étudiants sont retirées de la version diffusée."
                    ),
                    (
                        f"Prochaine réunion indicativement en {MOIS[(mois % 12)]} {annee if mois < 12 else annee + 1}. "
                        f"Le présent PV est transmis aux membres sous huit jours."
                    ),
                    _cloture(annee, rng.choice(LIEUX)),
                ],
            )
        )
    return pieces


def rapports(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    for i in range(n):
        date, annee, mois = _date(rng)
        trimestre = f"T{((mois - 1) // 3) + 1}"
        key, service = _service(rng)
        pieces.append(
            Piece(
                nom=f"rapport_{key}_{annee}_{trimestre}_{i:04d}.docx",
                service=service,
                ref=_ref(key[:3].upper(), "RAP", annee, i + 1),
                date=date,
                objet=f"Rapport d'activités {trimestre} {annee} — {service}",
                signataire=_signataire(rng),
                destinataires="Direction, conseil, archives",
                paragraphes=[
                    "## Contexte",
                    _intro(service, annee, "rapport d'activités"),
                    (
                        f"Durant {trimestre} {annee}, {service} a traité les dossiers courants, "
                        f"participé à {rng.randint(2, 8)} réunions institutionnelles et versé "
                        f"{rng.randint(12, 90)} pièces au Centre de documentation. "
                        f"Effectif mobilisé : {rng.randint(2, 14)} agents, hors vacataires."
                    ),
                    "## Réalisations",
                    (
                        f"Faits marquants : avancement du processus « {rng.choice(PROCESSUS)} » ; "
                        f"collaboration avec {rng.choice(PARTENAIRES)} ; "
                        f"session de formation de {rng.randint(8, 40)} participants. "
                        f"Dépenses engagées : {_montant(rng, 40_000, 1_800_000)}, imputées selon le plan {annee}."
                    ),
                    "## Difficultés",
                    (
                        f"Points de vigilance : {rng.choice(INCIDENTS)[0]} ; délais de versement encore irréguliers "
                        f"dans certains secrétariats ; {rng.choice(['PDF image', 'listes non anonymisées', 'doublons de fichiers'])}. "
                        f"Ces limites sont connues du prototype DocSearch et de la cellule qualité."
                    ),
                    "## Perspectives",
                    (
                        f"Pour le trimestre suivant : rattraper les versements, former deux correspondants, "
                        f"mettre à jour la procédure concernée. Le rapport détaillé chiffré reste à l'agence comptable."
                    ),
                    _cloture(annee, rng.choice(LIEUX)),
                ],
            )
        )
    return pieces


def conventions(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    for i in range(n):
        date, annee, mois = _date(rng)
        partenaire = PARTENAIRES[i % len(PARTENAIRES)]
        filiere = _filiere(rng)
        pieces.append(
            Piece(
                nom=f"convention_{annee}_{i:04d}.docx",
                service=SERVICES["stages"] if i % 2 == 0 else SERVICES["direction"],
                ref=_ref("STG" if i % 2 == 0 else "DIR", "CT", annee, i + 1),
                date=date,
                objet=f"Convention / avenant — IBAM et {partenaire}",
                signataire=PERSONNES["claire"] if i % 2 else PERSONNES["moussa"],
                destinataires=f"{partenaire}, archives, stages",
                paragraphes=[
                    "## Article 1 — Objet",
                    _intro(SERVICES["direction"], annee, "convention"),
                    (
                        f"La présente convention organise la coopération entre l'IBAM et {partenaire} "
                        f"pour l'accueil de stagiaires, l'échange de documentation professionnelle "
                        f"et, le cas échéant, des actions de formation continue. Filière prioritaire : {filiere}."
                    ),
                    "## Article 2 — Engagements",
                    (
                        "L'IBAM désigne un point focal (cellule des stages ou Centre de documentation). "
                        "Le partenaire accueille les étudiants dans le respect du secret professionnel. "
                        "Les rapports versés au fonds sont anonymisés lorsque des données de tiers apparaissent."
                    ),
                    "## Article 3 — Durée et avenant",
                    (
                        f"Durée : {rng.choice([1, 2, 3])} an(s) à compter de la signature, renouvelable. "
                        f"Un avenant pourra porter sur un accès lecture seule à DocSearch, "
                        f"sur autorisation expresse du conseil de l'institut."
                    ),
                    "## Article 4 — Litiges",
                    "Les parties privilégient la conciliation. À défaut, les juridictions de Ouagadougou sont compétentes.",
                    _cloture(annee, "campus principal, secteur 25"),
                ],
            )
        )
    return pieces


def circulaires_pdf(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    objets = [
        "droits d'inscription et modalités CampusFaso",
        "calendrier des examens et rattrapages",
        "discipline dans les salles de cours et d'examen",
        "usage du réseau et des postes documentaires",
        "conservation des copies et des PV",
        "hygiène et sécurité des salles",
        "communication officielle et affichage",
        "stages, mémoires et projets tutorés",
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        objet = objets[i % len(objets)]
        pieces.append(
            Piece(
                nom=f"circulaire_{annee}_{i:04d}.pdf",
                service=SERVICES["scolarite"] if i % 3 else SERVICES["direction"],
                ref=_ref("DIR", "CIR", annee, i + 1),
                date=date,
                objet=f"Circulaire — {objet} ({annee})",
                signataire=PERSONNES["claire"],
                destinataires="Tous services, délégués, affichage",
                paragraphes=[
                    _intro(SERVICES["direction"], annee, "circulaire"),
                    (
                        f"Le Directeur de l'IBAM porte à la connaissance de la communauté universitaire "
                        f"les dispositions relatives à : {objet}. "
                        f"Ces dispositions s'appliquent au campus principal et à Somgandé, formations du jour et du soir."
                    ),
                    (
                        f"Les chefs de service en assurent la diffusion. Les secrétariats versent un exemplaire "
                        f"signé au Centre de documentation. La version PDF texte est indexée dans DocSearch. "
                        f"Toute infraction expose aux sanctions prévues au règlement intérieur."
                    ),
                    (
                        f"Entrée en vigueur : {date}. Abrogation des circulaires contraires portant sur le même objet "
                        f"pour l'année {annee}. Renseignements : {MAIL['scolarite']} ou {MAIL['direction']}."
                    ),
                    _cloture(annee, rng.choice(LIEUX)),
                ],
            )
        )
    return pieces


def decisions_pdf(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    for i in range(n):
        date, annee, mois = _date(rng)
        sujet = rng.choice(
            [
                "ouverture d'une session de rattrapage",
                "affectation d'une salle à Somgandé",
                "autorisation d'un forum d'insertion",
                "achat de documentation professionnelle",
                "prolongation d'un pilote informatique",
                "nomination d'un correspondant versant",
                "fermeture exceptionnelle du magasin A",
                "validation d'un plan de numérisation",
            ]
        )
        pieces.append(
            Piece(
                nom=f"decision_{annee}_{i:04d}.pdf",
                service=SERVICES["direction"],
                ref=_ref("DIR", "DEC", annee, i + 1),
                date=date,
                objet=f"Décision du conseil / de la Direction — {sujet}",
                signataire="Le Directeur de l'IBAM",
                destinataires="Agence comptable, services concernés, archives",
                paragraphes=[
                    _intro(SERVICES["direction"], annee, "décision"),
                    (
                        f"Vu le règlement intérieur ; vu le PV du conseil ; vu l'avis de {rng.choice(SIGNATAIRES)} ; "
                        f"il est décidé ce qui suit : {sujet}, pour un montant le cas échéant de {_montant(rng, 50_000, 3_200_000)}, "
                        f"imputable sur le budget {annee}."
                    ),
                    (
                        "La présente décision est notifiée aux services. Elle est versée au fonds documentaire. "
                        "L'agence comptable n'exécute la dépense, s'il y a lieu, que sur bon visé. "
                        "Un compte rendu d'exécution est attendu à soixante jours."
                    ),
                    _cloture(annee, "salle conseil de l'institut"),
                ],
            )
        )
    return pieces


def devis_pdf(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    prestations = [
        ("fournitures de bureau", "ramettes, classeurs, étiquettes archives"),
        ("entretien climatisation", "révision splits magasin A et salle de lecture"),
        ("ouvrages professionnels", "lots CCA, OHADA, informatique de gestion"),
        ("maintenance serveur", "disques, mémoire, onduleur"),
        ("prestations d'impression", "brochures rentrée, affiches examens"),
        ("cablage réseau", "baie Somgandé et campus principal"),
        ("reliure et estampillage", "périodiques semestre écoulé"),
        ("formation externe", "archivage et sécurité de l'information"),
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        titre, detail = prestations[i % len(prestations)]
        montant = _montant(rng, 35_000, 1_900_000)
        pieces.append(
            Piece(
                nom=f"devis_{annee}_{i:04d}.pdf",
                service=SERVICES["agence"],
                ref=_ref("AC", "DEV", annee, i + 1),
                date=date,
                objet=f"Devis / bon de commande — {titre}",
                signataire=PERSONNES["boureima"],
                destinataires="Agence comptable, service demandeur, archives",
                paragraphes=[
                    _intro(SERVICES["agence"], annee, "pièce comptable"),
                    (
                        f"Prestataire fictif n° {2000 + i}. Objet : {titre} ({detail}). "
                        f"Lieu d'exécution : {rng.choice(LIEUX)}. Montant TTC : {montant}. "
                        f"Délai d'exécution : {rng.choice([7, 10, 15, 21, 30])} jours."
                    ),
                    (
                        "Trois devis sont joints lorsque le seuil réglementaire l'exige. "
                        "Imputation proposée sur la ligne 641 ou 643 selon le caractère documentaire ou informatique. "
                        "La liquidation F correspondante portera la même cote."
                    ),
                    (
                        "Cette pièce PDF est versée au dossier de marché interne. "
                        "Elle ne constitue pas un engagement vis-à-vis d'un tiers réel : "
                        "il s'agit d'une reconstitution pédagogique pour le prototype DocSearch."
                    ),
                    _cloture(annee, "agence comptable de l'IBAM"),
                ],
            )
        )
    return pieces


def listes_etudiants(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    codes = ["CCA", "ABF", "MG", "ADB", "MIAGE", "MISIE", "AGE"]
    for i in range(n):
        date, annee, mois = _date(rng, rng.choice([2020, 2021, 2022, 2023, 2024, 2025, 2026]))
        code = codes[i % len(codes)]
        niveau = rng.choice(NIVEAUX)
        regime = rng.choice(REGIMES)
        lignes = []
        for j in range(rng.randint(12, 28)):
            nom, prenom = _personne(rng)
            matricule = f"{code}-{niveau}-{annee % 100:02d}-{j + 1:03d}"
            lignes.append(
                [
                    matricule,
                    nom,
                    prenom,
                    code,
                    niveau,
                    regime,
                    _email(prenom, nom, etudiant=True),
                ]
            )
        pieces.append(
            Piece(
                nom=f"liste_{code.lower()}_{niveau.lower()}_{annee}_{i:04d}.csv",
                service=SERVICES["scolarite"],
                ref=_ref("SCOL", "LST", annee, i + 1),
                date=date,
                objet=f"Liste pédagogique {code} {niveau} {annee}-{annee + 1} (données fictives)",
                signataire=PERSONNES["aminata"],
                colonnes=["matricule", "nom", "prenom", "filiere", "niveau", "regime", "email"],
                lignes=lignes,
            )
        )
    return pieces


def registres_csv(rng: random.Random, n: int) -> list[Piece]:
    pieces: list[Piece] = []
    kinds = [
        "emprunts",
        "versements",
        "tickets",
        "commandes",
        "formations",
        "visiteurs",
        "inventaire",
        "presences",
    ]
    for i in range(n):
        date, annee, mois = _date(rng)
        kind = kinds[i % len(kinds)]
        if kind == "emprunts":
            colonnes = ["date", "cote", "titre", "emprunteur_fictif", "retour_prevu", "statut"]
            lignes = []
            for j in range(18):
                nom, prenom = _personne(rng)
                lignes.append(
                    [
                        f"{annee}-{mois:02d}-{(j % 28) + 1:02d}",
                        f"E{1 + (j % 5)}-{100 + j}",
                        rng.choice(
                            [
                                "Comptabilité générale OHADA",
                                "Systèmes d'information d'entreprise",
                                "Marketing des services",
                                "Introduction à l'archivage",
                                "Statistique appliquée",
                                "Droit des sociétés",
                            ]
                        ),
                        f"{prenom} {nom}",
                        f"{annee}-{mois:02d}-28",
                        rng.choice(["en cours", "rendu", "retard"]),
                    ]
                )
            objet = f"Registre des prêts — {MOIS[mois - 1]} {annee}"
            service = SERVICES["doc"]
            signataire = PERSONNES["fatou"]
        elif kind == "versements":
            colonnes = ["date", "service", "nb_pieces", "formats", "bordereau", "visa"]
            lignes = [
                [
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    rng.choice(list(SERVICES.values())),
                    str(rng.randint(3, 40)),
                    rng.choice(["PDF", "DOCX", "TXT", "CSV", "mixte"]),
                    f"BORD-{annee}-{i:03d}-{j:02d}",
                    rng.choice(["David Kaboré", "Fatou Sanou", "Issa Ouédraogo"]),
                ]
                for j in range(16)
            ]
            objet = f"Bordereaux de versement — {MOIS[mois - 1]} {annee}"
            service = SERVICES["doc"]
            signataire = PERSONNES["david"]
        elif kind == "tickets":
            colonnes = ["id", "date", "demandeur", "service", "objet", "priorite", "etat"]
            lignes = [
                [
                    f"T-{annee}-{i:03d}-{j:02d}",
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    f"{_personne(rng)[1]} {_personne(rng)[0]}",
                    rng.choice(list(SERVICES.values())),
                    rng.choice(
                        [
                            "poste bloqué",
                            "DocSearch inaccessible",
                            "imprimante documentation",
                            "compte CampusFaso",
                            "vidéo projecteur Somgandé",
                            "restauration fichier",
                        ]
                    ),
                    rng.choice(["basse", "normale", "haute"]),
                    rng.choice(["ouvert", "en cours", "clos"]),
                ]
                for j in range(20)
            ]
            objet = f"Registre des tickets DSI — {MOIS[mois - 1]} {annee}"
            service = SERVICES["dsi"]
            signataire = PERSONNES["ibrahim"]
        elif kind == "commandes":
            colonnes = ["ref", "date", "designation", "montant_fcfa", "imputation", "etat"]
            lignes = [
                [
                    f"BC-{annee}-{i:03d}-{j:02d}",
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    rng.choice(
                        [
                            "ramettes A4",
                            "classeurs archives",
                            "abonnements revues",
                            "pièces onduleur",
                            "badges visiteurs",
                            "reliure semestrielles",
                        ]
                    ),
                    str(rng.randrange(15_000, 900_000, 5_000)),
                    rng.choice(["641", "643", "618", "606"]),
                    rng.choice(["engagé", "livré", "soldé"]),
                ]
                for j in range(14)
            ]
            objet = f"Suivi des commandes documentaires et informatiques — {MOIS[mois - 1]} {annee}"
            service = SERVICES["agence"]
            signataire = PERSONNES["boureima"]
        elif kind == "formations":
            colonnes = ["code", "intitule", "date", "duree_j", "public", "lieu", "presents"]
            lignes = [
                [
                    f"F-{annee}-{i:02d}-{j:02d}",
                    rng.choice(
                        [
                            "Archivage numérique",
                            "Recherche DocSearch",
                            "Sécurité informatique",
                            "Rédaction administrative",
                            "Excel scolarité",
                            "Qualité documentaire",
                        ]
                    ),
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    str(rng.choice([1, 2, 3])),
                    rng.choice(["secrétariats", "enseignants", "documentation", "tous services"]),
                    rng.choice(LIEUX),
                    str(rng.randint(6, 42)),
                ]
                for j in range(10)
            ]
            objet = f"Sessions de formation interne — {MOIS[mois - 1]} {annee}"
            service = SERVICES["rh"]
            signataire = PERSONNES["mariam"]
        elif kind == "visiteurs":
            colonnes = ["date", "nom_fictif", "organisme", "motif", "badge", "sortie"]
            lignes = [
                [
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    f"{_personne(rng)[1]} {_personne(rng)[0]}",
                    rng.choice(PARTENAIRES),
                    rng.choice(["visite documentation", "forum", "audit", "livraison", "réunion"]),
                    f"BV-{annee}-{j:03d}",
                    rng.choice(["oui", "oui", "non"]),
                ]
                for j in range(16)
            ]
            objet = f"Registre d'accueil des visiteurs — {MOIS[mois - 1]} {annee}"
            service = SERVICES["direction"]
            signataire = PERSONNES["claire"]
        elif kind == "inventaire":
            colonnes = ["code", "designation", "quantite", "etat", "localisation", "service"]
            lignes = [
                [
                    f"INV-{annee}-{i:03d}-{j:02d}",
                    rng.choice(
                        [
                            "rayonnage archives",
                            "poste lecteur",
                            "scanner A4",
                            "extincteur",
                            "split climatisation",
                            "vidéoprojecteur",
                            "switch réseau",
                        ]
                    ),
                    str(rng.randint(1, 24)),
                    rng.choice(["bon", "moyen", "à réformer"]),
                    rng.choice(LIEUX),
                    rng.choice(list(SERVICES.values())),
                ]
                for j in range(15)
            ]
            objet = f"Inventaire partiel — {MOIS[mois - 1]} {annee}"
            service = SERVICES["dsi"]
            signataire = PERSONNES["ibrahim"]
        else:
            colonnes = ["date", "agent_fictif", "service", "plage", "motif", "visa"]
            lignes = [
                [
                    f"{annee}-{mois:02d}-{(j % 27) + 1:02d}",
                    f"{_personne(rng)[1]} {_personne(rng)[0]}",
                    rng.choice(list(SERVICES.values())),
                    rng.choice(["7h30-15h30", "8h-16h", "18h-21h", "samedi matin"]),
                    rng.choice(["service normal", "astreinte documentation", "surveillance examen", "formation"]),
                    rng.choice(["Mariam Traoré", "Claire Nikièma", "Fatou Sanou"]),
                ]
                for j in range(18)
            ]
            objet = f"Feuille de présence / astreintes — {MOIS[mois - 1]} {annee}"
            service = SERVICES["rh"]
            signataire = PERSONNES["mariam"]

        pieces.append(
            Piece(
                nom=f"registre_{kind}_{annee}_{i:04d}.csv",
                service=service,
                ref=_ref("REG", kind[:3].upper(), annee, i + 1),
                date=date,
                objet=objet,
                signataire=signataire,
                colonnes=colonnes,
                lignes=lignes,
            )
        )
    return pieces


def pieces() -> list[Piece]:
    rng = random.Random(SEED)
    ensemble = (
        notes_de_service(rng, 360)
        + convocations(rng, 40)
        + comptes_rendus_incidents(rng, 40)
        + procedures(rng, 30)
        + faq_thematiques(rng, 20)
        + proces_verbaux(rng, 120)
        + rapports(rng, 40)
        + conventions(rng, 30)
        + circulaires_pdf(rng, 80)
        + decisions_pdf(rng, 50)
        + devis_pdf(rng, 40)
        + listes_etudiants(rng, 50)
        + registres_csv(rng, 110)
    )
    if len(ensemble) != CIBLE:
        raise SystemExit(f"Expansion : {len(ensemble)} pièces au lieu de {CIBLE}.")
    return ensemble
