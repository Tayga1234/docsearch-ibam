from .identite import MAIL, PERSONNES, SERVICES
from .modele import Piece


def pieces() -> list[Piece]:
    return [
        Piece(
            nom="projet_tutore_indexation.txt",
            service=SERVICES["st"],
            ref="IBAM/ST/PT/2025/MISIE-04",
            date="12 janvier 2025",
            objet="Cahier des charges du projet tutoré — indexation intelligente du fonds IBAM",
            signataire=PERSONNES["adama"],
            destinataires="Étudiant KOROGO, Centre de documentation, DSI",
            paragraphes=[
                "Le projet tutoré du Master MISIE confié à Gaëtan KOROGO (et binôme le cas échéant) consiste à concevoir et démontrer un portail local capable d'indexer des pièces hétérogènes du Centre de documentation de l'IBAM, puis de les rechercher par mots-clés, par similarité de contenu et de façon hybride.",
                "Contraintes : hébergement sur le campus, pas de cloud obligatoire, formats PDF, DOCX, CSV, TXT, authentification simple (profil lecteur / administrateur), temps de réponse inférieur à la seconde sur un fonds d'une centaine de pièces, interface en français.",
                "Livrables : prototype DocSearch, corpus reconstitué d'environ 100 pièces du cas IBAM, documentation d'installation, tests, soutenance. Encadrement métier : Fatou Sanou. Encadrement technique : Ibrahim Ouédraogo. Encadrement académique : Adama Ouédraogo et Rasmané Ilboudo.",
                "Jalons : cadrage 15 janvier ; corpus v1 fin février ; pilote métier 15 mars ; gel fonctionnel 15 juin ; soutenance 24 juillet 2025.",
                "Le code et le fonds de démonstration restent propriété pédagogique de l'IBAM / UJKZ. Les données nominatives réelles d'étudiants ne doivent pas y figurer.",
            ],
        ),
        Piece(
            nom="politique_qualite_ibam.txt",
            service=SERVICES["qualite"],
            ref="IBAM/QUAL/POL/2025/001",
            date="24 janvier 2025",
            objet="Politique qualité 2025 — scolarité, documentation, systèmes d'information",
            signataire=PERSONNES["paulin"],
            destinataires="Direction, chefs de service",
            paragraphes=[
                "La cellule qualité de l'IBAM retient trois engagements pour 2025 : (1) délivrer une attestation de scolarité en 48 heures dans 90 % des cas ; (2) indexer une pièce versée en 48 heures dans 85 % des cas ; (3) rétablir un incident bloquant DSI en 4 heures ouvrées dans 80 % des cas.",
                "Les indicateurs sont extraits des registres scolarité, du bordereau d'archives et du tableau de tickets. Un tableau de bord trimestriel est présenté au conseil et versé à DocSearch sous cote QUAL-TB.",
                "Les non-conformités récurrentes 2024 — PDF image, listes nominatives trop riches, sujets d'examen déposés hors délai — font l'objet d'actions : procédure 2.1, note d'anonymisation, circulaire examens.",
                "Tout agent peut signaler une non-conformité à qualite.ibam@ujkz.bf. Les signalements de bonne foi ne sont pas sanctionnés.",
            ],
        ),
        Piece(
            nom="alerte_qualite_documents.txt",
            service=SERVICES["qualite"],
            ref="IBAM/QUAL/AL/2025/004",
            date="20 février 2025",
            objet="Alerte qualité — PDF scannés non exploitables par le portail documentaire",
            signataire=PERSONNES["paulin"],
            destinataires="Tous les services versants",
            paragraphes=[
                "Constat : sur 22 PDF versés entre le 3 et le 18 février, 7 étaient des images sans couche texte. DocSearch ne peut alors ni résumer, ni étiqueter, ni rechercher le contenu. L'usager croit le document absent.",
                "Mesure immédiate : David Kaboré retourne ces fichiers. Mesure durable : privilégier l'export PDF depuis Word, ou un passage OCR (DSI) avant versement. Les scans de signatures seules en dernière page restent acceptables si le corps est du texte.",
                "Les secrétariats de Somgandé, qui photocopient encore beaucoup de notes, sont particulièrement concernés. Un créneau d'accompagnement est ouvert les jeudis 14 h – 16 h au magasin A.",
                "Indicateur suivi : taux de PDF sans texte, cible < 10 % au troisième trimestre.",
            ],
        ),
        Piece(
            nom="charte_stagiaire_ibam.txt",
            service=SERVICES["stages"],
            ref="IBAM/STG/CHARTE/2025/001",
            date="29 janvier 2025",
            objet="Charte du stagiaire IBAM — droits, devoirs, restitution documentaire",
            signataire=PERSONNES["moussa"],
            destinataires="Étudiants, tuteurs entreprises, tuteurs IBAM",
            paragraphes=[
                "Le stagiaire représente l'IBAM dans l'entreprise ou l'administration d'accueil. Il respecte le règlement intérieur de celle-ci, l'horaire convenu et la confidentialité des données. Il n'emporte pas de fichiers nominatifs hors du site d'accueil sans autorisation écrite.",
                "Une convention tripartite (étudiant, IBAM, accueil) est signée avant J1. Le tuteur IBAM est un enseignant de la filière ; le suivi administratif relève de Moussa Compaoré. Le rapport est déposé en version PDF texte au Centre de documentation dans les quinze jours après la soutenance.",
                "Pour les stages effectués à l'IBAM même (cas DocSearch), le stagiaire est soumis à la charte informatique et à la procédure d'archivage. Il n'administre pas l'index sans présence du correspondant DSI après la fin du stage, sauf décision contraire.",
                "Les absences se justifient comme en formation. Trois absences non justifiées peuvent entraîner la rupture de la convention, après entretien.",
                f"Modèle de convention : secrétariat des stages — {MAIL['stages']}.",
            ],
        ),
        Piece(
            nom="suivi_conventions_stage.txt",
            service=SERVICES["stages"],
            ref="IBAM/STG/SUIVI/2025/T1",
            date="31 mars 2025",
            objet="Suivi des conventions de stage — premier trimestre 2025",
            signataire=PERSONNES["moussa"],
            destinataires="Départements, scolarité, documentation",
            paragraphes=[
                "Au 31 mars 2025, 41 conventions sont actives : 18 MIAGE/MISIE, 9 CCA, 6 ABF, 5 MG, 3 ADB. Terrains : Ouagadougou (32), Koudougou (4), Bobo-Dioulasso (5). Deux conventions sont en attente de visa entreprise depuis plus de trois semaines (relances en cours).",
                "Le stage DocSearch au Centre de documentation (KOROGO, MISIE) court du 13 janvier au 18 avril, avec possibilité de prolongation jusqu'à la soutenance de juillet pour la maintenance de l'index.",
                "Sept rapports 2024 n'ont toujours pas été versés au format PDF texte. Les étudiants concernés ne pourront retirer leur attestation de succès de stage tant que Fatou Sanou n'aura pas émargé le versement.",
                "Une journée de restitution des stages MIAGE/MISIE est prévue le 16 mai 2025, amphithéâtre A, 14 h. Les employeurs partenaires sont conviés.",
            ],
        ),
    ]
