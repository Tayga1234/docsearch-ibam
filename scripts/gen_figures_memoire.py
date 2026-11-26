"""Génère les figures du mémoire (PNG) avec Pillow."""

from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rapport" / "figures"
RAW = ROOT / "data" / "raw"
NAVY = (26, 54, 93)
WHITE = (255, 255, 255)
LIGHT = (232, 239, 248)
ACCENT = (47, 111, 176)
GRAY = (80, 80, 80)
BG = (255, 255, 255)
GOLD = (196, 163, 90)
TEAL = (56, 128, 128)
ROSE = (168, 90, 90)
SAGE = (90, 132, 90)
SKY = (123, 163, 212)


def font(size: int, bold: bool = False):
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_box(draw, xy, fill, outline, width=2, radius=12):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, xy, text, fnt, fill=NAVY):
    x1, y1, x2, y2 = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), text, font=fnt, fill=fill)


def arrow_right(draw, x1, y, x2):
    draw.line((x1, y, x2 - 10, y), fill=ACCENT, width=4)
    draw.polygon([(x2, y), (x2 - 12, y - 7), (x2 - 12, y + 7)], fill=ACCENT)


def arrow_down(draw, x, y1, y2):
    draw.line((x, y1, x, y2 - 10), fill=ACCENT, width=4)
    draw.polygon([(x, y2), (x - 7, y2 - 12), (x + 7, y2 - 12)], fill=ACCENT)


def fig_pipeline():
    img = Image.new("RGB", (1400, 420), BG)
    draw = ImageDraw.Draw(img)
    fnt = font(22, True)
    steps = [
        "Fichiers\nPDF DOCX\nCSV TXT",
        "Extraction\ndu texte",
        "Enrichissement\ntags résumé\nentités",
        "Stockage\nSQLite +\nWhoosh",
        "Recherche\nmots-clés\nsémantique hybride",
        "Interface\nweb",
    ]
    w, h, gap, x0, y0 = 190, 170, 28, 40, 120
    for i, label in enumerate(steps):
        x = x0 + i * (w + gap)
        rounded_box(draw, (x, y0, x + w, y0 + h), LIGHT, NAVY)
        lines = label.split("\n")
        ty = y0 + 28
        for j, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=fnt)
            tw = bbox[2] - bbox[0]
            draw.text((x + (w - tw) / 2, ty + j * 32), line, font=fnt, fill=NAVY)
        if i < len(steps) - 1:
            arrow_right(draw, x + w + 2, y0 + h / 2, x + w + gap - 2)
    title = font(20, True)
    draw.text((40, 30), "Figure 1. Pipeline d'indexation intelligente", font=title, fill=NAVY)
    img.save(OUT / "fig1_pipeline.png", "PNG")


def fig_architecture():
    img = Image.new("RGB", (1200, 780), BG)
    draw = ImageDraw.Draw(img)
    title = font(20, True)
    fnt = font(22, True)
    small = font(18)
    draw.text((40, 24), "Figure 2. Architecture logique de DocSearch", font=title, fill=NAVY)
    layers = [
        (70, "Présentation — interface React (recherche, résultats, fiche, téléversement)"),
        (200, "API REST — FastAPI, validation Pydantic, documentation OpenAPI"),
        (330, "Métier — ingestion, extraction, enrichissement, indexation, recherche"),
        (460, "Stockage — fichiers bruts, SQLite (métadonnées), index Whoosh"),
    ]
    for y, text in layers:
        rounded_box(draw, (80, y, 1120, y + 100), LIGHT, NAVY)
        center_text(draw, (80, y, 1120, y + 100), text, fnt)
    for y in (170, 300, 430):
        arrow_down(draw, 600, y, y + 30)
    draw.text((80, 600), "Le client n'accède jamais directement à l'index : toute requête passe par l'API.", font=small, fill=GRAY)
    img.save(OUT / "fig2_architecture.png", "PNG")


def fig_hybride():
    img = Image.new("RGB", (1200, 620), BG)
    draw = ImageDraw.Draw(img)
    title = font(20, True)
    fnt = font(20, True)
    draw.text((40, 24), "Figure 3. Fusion des scores en recherche hybride", font=title, fill=NAVY)
    rounded_box(draw, (80, 90, 520, 210), LIGHT, NAVY)
    center_text(draw, (80, 90, 520, 210), "Requête utilisateur", fnt)
    arrow_down(draw, 300, 210, 250)
    rounded_box(draw, (80, 260, 300, 400), LIGHT, NAVY)
    center_text(draw, (80, 260, 300, 400), "Whoosh\n(mots-clés, poids 0,6)", fnt)
    rounded_box(draw, (340, 260, 560, 400), LIGHT, NAVY)
    center_text(draw, (340, 260, 560, 400), "TF-IDF\n(similarité, poids 0,4)", fnt)
    arrow_down(draw, 190, 400, 450)
    arrow_down(draw, 450, 400, 450)
    rounded_box(draw, (80, 460, 560, 580), LIGHT, ACCENT)
    center_text(draw, (80, 460, 560, 580), "Score combiné et liste classée", fnt, WHITE)
    rounded_box(draw, (620, 260, 1120, 580), LIGHT, NAVY)
    note = (
        "Normalisation des scores\n"
        "puis combinaison linéaire.\n\n"
        "L'extrait lexical est conservé\n"
        "en priorité (surbrillance).\n\n"
        "Mode par défaut de\n"
        "démonstration : hybride."
    )
    draw.multiline_text((660, 300), note, font=fnt, fill=NAVY, spacing=8)
    img.save(OUT / "fig3_hybride.png", "PNG")


def _text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        tw, _ = _text_size(draw, trial, fnt)
        if tw <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [text]


def _stick_actor(draw, x, y, label, fnt):
    """Acteur UML : bonhomme bâton + nom (éventuellement sur deux lignes)."""
    r = 22
    draw.ellipse((x - r, y, x + r, y + 2 * r), outline=NAVY, width=3)
    body_top = y + 2 * r
    body_bot = body_top + 70
    draw.line((x, body_top, x, body_bot), fill=NAVY, width=3)
    draw.line((x - 38, body_top + 28, x + 38, body_top + 28), fill=NAVY, width=3)
    draw.line((x, body_bot, x - 32, body_bot + 48), fill=NAVY, width=3)
    draw.line((x, body_bot, x + 32, body_bot + 48), fill=NAVY, width=3)
    ly = body_bot + 52
    for line in label.split("\n"):
        tw, th = _text_size(draw, line, fnt)
        draw.text((x - tw / 2, ly), line, font=fnt, fill=NAVY)
        ly += th + 2
    return x, body_top + 28


def _ellipse_uc(draw, cx, cy, text, fnt, rx=168, ry=48):
    box = (cx - rx, cy - ry, cx + rx, cy + ry)
    draw.ellipse(box, fill=LIGHT, outline=NAVY, width=3)
    lines = _wrap(draw, text, fnt, int(rx * 1.7))
    total_h = len(lines) * 22
    ty = cy - total_h / 2
    for line in lines:
        tw, th = _text_size(draw, line, fnt)
        draw.text((cx - tw / 2, ty), line, font=fnt, fill=NAVY)
        ty += 22
    return cx, cy, rx, ry


def _edge_from_actor(draw, ax, ay, cx, cy, rx, ry):
    """Segment acteur → bord de l'ellipse."""
    dx, dy = cx - ax, cy - ay
    dist = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / dist, dy / dist
    # intersection ellipse: point = c - (rx,ry) scaled along unit vector
    # x^2/rx^2 + y^2/ry^2 = 1
    denom = ((ux * ux) / (rx * rx) + (uy * uy) / (ry * ry)) ** 0.5 or 1
    px = cx - ux / denom
    py = cy - uy / denom
    draw.line((ax, ay, px, py), fill=NAVY, width=2)


def _generalization(draw, x_child, y_child, x_parent, y_parent):
    """Héritage UML vertical : triangle creux vers le parent (haut)."""
    draw.line((x_child, y_child, x_parent, y_parent + 18), fill=NAVY, width=2)
    draw.polygon(
        [
            (x_parent, y_parent),
            (x_parent - 12, y_parent + 20),
            (x_parent + 12, y_parent + 20),
        ],
        outline=NAVY,
        fill=WHITE,
    )
    draw.line(
        [(x_parent, y_parent), (x_parent - 12, y_parent + 20), (x_parent + 12, y_parent + 20), (x_parent, y_parent)],
        fill=NAVY,
        width=2,
    )


def _generalization_h(draw, x_child, y, x_parent):
    """Héritage UML horizontal : triangle creux vers le parent (à gauche)."""
    tip_dir = 1 if x_parent < x_child else -1
    base = x_parent + 20 * tip_dir
    draw.line((x_child, y, base, y), fill=NAVY, width=2)
    draw.polygon(
        [(x_parent, y), (base, y - 12), (base, y + 12)],
        outline=NAVY,
        fill=WHITE,
    )
    draw.line([(x_parent, y), (base, y - 12), (base, y + 12), (x_parent, y)], fill=NAVY, width=2)


def _ellipse_border(cx, cy, rx, ry, tx, ty):
    """Point du bord de l'ellipse dans la direction d'un autre point."""
    dx, dy = tx - cx, ty - cy
    dist = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / dist, dy / dist
    denom = ((ux * ux) / (rx * rx) + (uy * uy) / (ry * ry)) ** 0.5 or 1
    return cx + ux / denom, cy + uy / denom


def _dashed_line(draw, p1, p2, fill, width=2, dash=9, gap=6):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / length, dy / length
    t = 0.0
    while t < length:
        t2 = min(t + dash, length)
        draw.line((x1 + ux * t, y1 + uy * t, x1 + ux * t2, y1 + uy * t2), fill=fill, width=width)
        t += dash + gap


def _open_arrow(draw, x1, y1, x2, y2, fill, size=11):
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    p1 = (x2 - ux * size + px * size * 0.5, y2 - uy * size + py * size * 0.5)
    p2 = (x2 - ux * size - px * size * 0.5, y2 - uy * size - py * size * 0.5)
    draw.line((p1[0], p1[1], x2, y2), fill=fill, width=2)
    draw.line((p2[0], p2[1], x2, y2), fill=fill, width=2)


def _uc_relation(draw, src, dst, stereotype, fnt, fill=NAVY):
    """Flèche pointillée UML entre deux cas (include vers l'inclus, extend vers la base)."""
    x1, y1 = _ellipse_border(src[0], src[1], src[2], src[3], dst[0], dst[1])
    x2, y2 = _ellipse_border(dst[0], dst[1], dst[2], dst[3], src[0], src[1])
    _dashed_line(draw, (x1, y1), (x2, y2), fill)
    _open_arrow(draw, x1, y1, x2, y2, fill)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5 or 1
    nx, ny = -dy / dist, dx / dist
    if abs(ny) < 0.3:
        nx, ny = 0, -1
    label = f"«{stereotype}»"
    tw, th = _text_size(draw, label, fnt)
    draw.text((mx + nx * 18 - tw / 2, my + ny * 16 - th / 2), label, font=fnt, fill=fill)


def _package(draw, box, title, fill, fnt):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=ACCENT, width=2)
    tw, th = _text_size(draw, title, fnt)
    x1, y1, _, _ = box
    draw.rectangle((x1 + 12, y1 - 2, x1 + 20 + tw, y1 + th + 8), fill=WHITE, outline=ACCENT, width=1)
    draw.text((x1 + 16, y1 + 2), title, font=fnt, fill=NAVY)


def _note(draw, xy, lines, fnt):
    x1, y1, x2, y2 = xy
    fold = 18
    draw.polygon(
        [(x1, y1), (x2 - fold, y1), (x2, y1 + fold), (x2, y2), (x1, y2)],
        fill=(255, 252, 235),
        outline=GRAY,
    )
    draw.line((x2 - fold, y1, x2 - fold, y1 + fold, x2, y1 + fold), fill=GRAY, width=1)
    ty = y1 + 12
    for line in lines:
        draw.text((x1 + 12, ty), line, font=fnt, fill=GRAY)
        ty += 20


def fig_cas_utilisation():
    """Diagramme de cas d'utilisation UML de DocSearch (niveau master)."""
    img = Image.new("RGB", (2040, 1320), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(22, True)
    actor_f = font(18, True)
    uc_f = font(16, True)
    pkg_f = font(15, True)
    small = font(15)
    stereo_f = font(14, True)
    draw.text((40, 16), "Diagramme de cas d'utilisation — DocSearch", font=title_f, fill=NAVY)

    sys = (380, 58, 1660, 1110)
    draw.rectangle(sys, outline=NAVY, width=3)
    sys_label = "DocSearch"
    tw, _ = _text_size(draw, sys_label, title_f)
    draw.rectangle((sys[0] + 16, sys[1] - 2, sys[0] + 26 + tw, sys[1] + 34), fill=WHITE)
    draw.text((sys[0] + 22, sys[1] + 4), sys_label, font=title_f, fill=NAVY)

    _package(draw, (400, 100, 1000, 1070), "Consultation", (237, 244, 252), pkg_f)
    _package(draw, (1030, 100, 1630, 1070), "Administration de l'index", (247, 242, 232), pkg_f)

    ux, uy = _stick_actor(draw, 165, 300, "Utilisateur\n(lecteur)", actor_f)
    ax, ay = _stick_actor(draw, 1875, 300, "Administrateur\n(documentaliste)", actor_f)

    rx, ry = 128, 46
    auth = _ellipse_uc(draw, 700, 190, "S'authentifier", uc_f, rx=rx, ry=ry)
    search = _ellipse_uc(draw, 540, 370, "Rechercher un document", uc_f, rx=rx, ry=ry)
    compare = _ellipse_uc(draw, 860, 370, "Comparer les trois modes", uc_f, rx=rx, ry=ry)
    consult = _ellipse_uc(draw, 540, 560, "Consulter une fiche", uc_f, rx=rx, ry=ry)
    export = _ellipse_uc(draw, 860, 560, "Exporter une fiche", uc_f, rx=rx, ry=ry)
    browse = _ellipse_uc(draw, 540, 760, "Parcourir le fonds", uc_f, rx=rx, ry=ry)

    scan = _ellipse_uc(draw, 1490, 200, "Scanner le dossier", uc_f, rx=rx, ry=ry)
    upload = _ellipse_uc(draw, 1490, 430, "Téléverser des documents", uc_f, rx=rx, ry=ry)
    index = _ellipse_uc(draw, 1185, 315, "Indexer et enrichir le document", uc_f, rx=145, ry=50)
    delete = _ellipse_uc(draw, 1490, 660, "Supprimer un document", uc_f, rx=rx, ry=ry)
    rebuild = _ellipse_uc(draw, 1490, 860, "Reconstruire l'index", uc_f, rx=rx, ry=ry)

    for geom in (auth, search, consult, browse):
        _edge_from_actor(draw, ux + 42, uy, geom[0], geom[1], geom[2], geom[3])
    for geom in (scan, upload, delete, rebuild):
        _edge_from_actor(draw, ax - 42, ay, geom[0], geom[1], geom[2], geom[3])

    _uc_relation(draw, compare, search, "extend", stereo_f, ACCENT)
    _uc_relation(draw, export, consult, "extend", stereo_f, ACCENT)
    _uc_relation(draw, scan, index, "include", stereo_f, NAVY)
    _uc_relation(draw, upload, index, "include", stereo_f, NAVY)

    _note(
        draw,
        (430, 900, 960, 1045),
        [
            "{ précondition : session authentifiée }",
            "«extend» : comportement optionnel",
            "«include» : fragment obligatoire",
            "du pipeline d'indexation intelligente.",
        ],
        small,
    )

    gy = 1155
    _generalization_h(draw, 1875, gy, 165)

    draw.line((50, 1210, 140, 1210), fill=NAVY, width=2)
    draw.text((155, 1198), "Association", font=small, fill=GRAY)
    _generalization_h(draw, 430, 1210, 310)
    draw.text((445, 1198), "Généralisation (héritage des cas lecteur)", font=small, fill=GRAY)
    _dashed_line(draw, (980, 1210), (1070, 1210), ACCENT)
    _open_arrow(draw, 980, 1210, 1070, 1210, ACCENT)
    draw.text((1080, 1198), "«extend» / «include»", font=small, fill=GRAY)

    img.save(OUT / "fig4_cas_utilisation.png", "PNG")


def _check(draw, x, y, size=16):
    """Coche verte dans un carré."""
    box = (x, y, x + size, y + size)
    draw.rounded_rectangle(box, radius=3, fill=(214, 245, 227), outline=(22, 128, 72), width=2)
    draw.line((x + 3, y + size * 0.55, x + size * 0.38, y + size - 4), fill=(22, 128, 72), width=3)
    draw.line((x + size * 0.38, y + size - 4, x + size - 3, y + 4), fill=(22, 128, 72), width=3)


def fig_grille_tests():
    """Grille de tests manuels cochée (figure 21)."""
    rows = [
        ("T-01", "Chargement initial", "Page de connexion DocSearch affichée"),
        ("T-02", "Consultation publique", "Accès recherche / fonds, pas d'administration"),
        ("T-03", "Authentification administrateur", "Menu Documents et Indexation visibles"),
        ("T-10", "Scan du dossier", "Compteur porté à 1 110 documents"),
        ("T-13", "Téléversement TXT", "Nouveau document dans la liste Documents"),
        ("T-14", "Format refusé (.png)", "Message d'erreur, pas d'ajout"),
        ("T-15", "Garde-fou import", "Dialogue de confirmation avant l'envoi"),
        ("T-20", "Recherche mots-clés", "Document pertinent, terme surligné"),
        ("T-23", "Recherche sémantique", "Classement par proximité de vocabulaire"),
        ("T-24", "Recherche hybride", "Résultats avec score, mode par défaut"),
        ("T-25", "Requête sans résultat", "Message « aucun résultat », pas de crash"),
        ("T-27", "Recherche vide", "Pas de crash, formulaire inchangé"),
        ("T-30", "Ouverture de fiche", "Résumé, tags et contenu visibles"),
        ("T-32", "Export de fiche", "Fichier texte téléchargé"),
        ("T-36", "Suppression (Documents)", "Saisie de SUPPRIMER exigée, document retiré"),
        ("T-37", "Reconstruction d'index", "Saisie de RECONSTRUIRE exigée, index recréé"),
        ("T-40", "Lisibilité", "Contrastes et interlignes suffisants"),
        ("T-45", "Cohérence visuelle", "Thèmes et pages homogènes"),
    ]
    header_h, row_h, top = 52, 38, 118
    W, H = 1680, top + header_h + row_h * len(rows) + 70
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(22, True)
    head_f = font(15, True)
    cell_f = font(14)
    small = font(14)
    draw.text((40, 22), "Figure 21. Grille de tests manuels cochée — DocSearch", font=title_f, fill=NAVY)
    draw.text(
        (40, 58),
        "Session du 27 octobre 2026  ·  Testeur : KOROGO Wendkuuni Ange Gaëtan  ·  Version 0.7.0  ·  18 / 18 OK",
        font=small,
        fill=GRAY,
    )

    cols = [(40, 110), (150, 430), (580, 920), (1500, 140)]
    headers = ["ID", "Scénario", "Résultat observé", "OK"]
    y0 = top
    draw.rectangle((36, y0, W - 36, y0 + header_h + row_h * len(rows)), outline=NAVY, width=2)
    draw.rectangle((36, y0, W - 36, y0 + header_h), fill=NAVY)
    for (x, _w), label in zip(cols, headers):
        draw.text((x + 10, y0 + 14), label, font=head_f, fill=WHITE)

    for i, (tid, scenario, result) in enumerate(rows):
        y = y0 + header_h + i * row_h
        if i % 2 == 0:
            draw.rectangle((37, y, W - 37, y + row_h), fill=LIGHT)
        draw.line((37, y, W - 37, y), fill=(210, 218, 230), width=1)
        draw.text((cols[0][0] + 10, y + 10), tid, font=head_f, fill=NAVY)
        draw.text((cols[1][0] + 10, y + 10), scenario, font=cell_f, fill=NAVY)
        draw.text((cols[2][0] + 10, y + 10), result, font=cell_f, fill=GRAY)
        _check(draw, cols[3][0] + 48, y + 10, 18)

    draw.text(
        (40, H - 42),
        "Aucune anomalie bloquante. Les actions destructives (suppression, reconstruction) sont protégées par confirmation textuelle.",
        font=small,
        fill=GRAY,
    )
    img.save(OUT / "fig21_grille_tests.png", "PNG")


def _fr_int(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def _fr_num(n: float, decimals: int = 2) -> str:
    return f"{n:.{decimals}f}".replace(".", ",")


def _text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _classify_piece(name: str) -> str:
    stem = name.lower()
    if stem.startswith("note_"):
        return "Notes de service"
    if stem.startswith("pv_"):
        return "Procès-verbaux"
    if stem.startswith("registre_"):
        return "Registres CSV"
    if stem.startswith("liste_"):
        return "Listes pédagogiques"
    if stem.startswith(("circulaire_", "decision_", "devis_")):
        return "Circulaires, décisions, devis"
    if stem.startswith(("convention_", "rapport_")):
        return "Conventions et rapports"
    if stem.startswith(("procedure_", "faq_", "convocation_", "incident_")):
        return "Procédures, FAQ, incidents"
    return "Noyau métier (pièces uniques)"


def corpus_files() -> list[Path]:
    if not RAW.exists():
        return []
    return [
        path
        for path in RAW.iterdir()
        if path.is_file() and path.name != ".gitkeep" and path.suffix.lower() in {".txt", ".pdf", ".docx", ".csv"}
    ]


def fig_corpus_formats():
    files = corpus_files()
    counts = Counter(path.suffix.lower() for path in files)
    slices = [
        (".txt", "TXT — notes et procédures", counts.get(".txt", 0), NAVY),
        (".docx", "DOCX — PV, rapports, conventions", counts.get(".docx", 0), ACCENT),
        (".pdf", "PDF — circulaires et pièces signées", counts.get(".pdf", 0), GOLD),
        (".csv", "CSV — listes et registres", counts.get(".csv", 0), TEAL),
    ]
    total = sum(item[2] for item in slices) or 1

    img = Image.new("RGB", (1400, 720), BG)
    draw = ImageDraw.Draw(img)
    title_f, body_f, big_f = font(22, True), font(20), font(28, True)
    draw.text((48, 28), "Répartition du corpus par format", font=title_f, fill=NAVY)

    cx, cy, r = 380, 390, 230
    start = -90
    for _, _, value, color in slices:
        extent = 360 * value / total
        draw.pieslice((cx - r, cy - r, cx + r, cy + r), start, start + extent, fill=color, outline=WHITE)
        start += extent
    hole = int(r * 0.58)
    draw.ellipse((cx - hole, cy - hole, cx + hole, cy + hole), fill=WHITE)
    center_text(draw, (cx - 110, cy - 50, cx + 110, cy + 8), _fr_int(total), big_f, NAVY)
    center_text(draw, (cx - 110, cy + 8, cx + 110, cy + 48), "pièces", body_f, GRAY)

    lx, ly = 760, 220
    for _, label, value, color in slices:
        pct = 100 * value / total
        draw.rounded_rectangle((lx, ly, lx + 36, ly + 36), radius=6, fill=color)
        draw.text((lx + 52, ly + 4), f"{label}", font=body_f, fill=NAVY)
        draw.text((lx + 52, ly + 32), f"{_fr_int(value)} fichiers  ·  {_fr_num(pct, 1)} %", font=font(16), fill=GRAY)
        ly += 78

    img.save(OUT / "fig23_corpus_formats.png", "PNG")


def fig_corpus_types():
    files = corpus_files()
    counts = Counter(_classify_piece(path.name) for path in files)
    order = [
        "Notes de service",
        "Procès-verbaux",
        "Registres CSV",
        "Listes pédagogiques",
        "Circulaires, décisions, devis",
        "Conventions et rapports",
        "Procédures, FAQ, incidents",
        "Noyau métier (pièces uniques)",
    ]
    rows = [(label, counts.get(label, 0)) for label in order if counts.get(label, 0)]
    maximum = max((n for _, n in rows), default=1)

    img = Image.new("RGB", (1400, 780), BG)
    draw = ImageDraw.Draw(img)
    title_f, body_f, small = font(22, True), font(18), font(16)
    draw.text((48, 28), "Composition du fonds par type de pièce", font=title_f, fill=NAVY)

    left, top, right, bottom = 420, 110, 1320, 720
    bar_h = 48
    gap = 22
    colors = [NAVY, ACCENT, TEAL, GOLD, ROSE, SAGE, SKY, GRAY]
    for i, (label, value) in enumerate(rows):
        y = top + i * (bar_h + gap)
        width = int((right - left) * value / maximum)
        draw.text((48, y + 10), label, font=body_f, fill=NAVY)
        draw.rounded_rectangle((left, y, left + max(width, 8), y + bar_h), radius=8, fill=colors[i % len(colors)])
        draw.text((left + width + 14, y + 12), _fr_int(value), font=small, fill=NAVY)

    img.save(OUT / "fig24_corpus_types.png", "PNG")


def fig_latences():
    modes = ["Mots-clés", "Sémantique", "Hybride"]
    series = [
        ("Moyenne", [37.04, 99.87, 82.22], ACCENT),
        ("P95", [51.20, 463.50, 99.60], GOLD),
        ("Maximum", [51.20, 463.50, 99.60], ROSE),
    ]
    ymax = 520

    img = Image.new("RGB", (1400, 760), BG)
    draw = ImageDraw.Draw(img)
    title_f, body_f, small = font(22, True), font(18), font(15)
    draw.text((48, 28), "Latence de recherche par mode (ms)", font=title_f, fill=NAVY)
    draw.text(
        (48, 64),
        "Le pic sémantique correspond à la première requête (construction de la matrice TF-IDF).",
        font=small,
        fill=GRAY,
    )

    left, top, right, bottom = 120, 140, 1320, 640
    draw.line((left, bottom, right, bottom), fill=NAVY, width=2)
    draw.line((left, top, left, bottom), fill=NAVY, width=2)
    for tick in (0, 100, 200, 300, 400, 500):
        y = bottom - int((bottom - top) * tick / ymax)
        draw.line((left, y, right, y), fill=LIGHT, width=1)
        label = str(tick)
        tw, _ = _text_size(draw, label, small)
        draw.text((left - 16 - tw, y - 10), label, font=small, fill=GRAY)

    group_w = (right - left) / len(modes)
    bar_w = 70
    for i, mode in enumerate(modes):
        gx = left + i * group_w
        cx = gx + group_w / 2
        for j, (_, values, color) in enumerate(series):
            h = int((bottom - top) * values[i] / ymax)
            x1 = cx - 1.5 * bar_w + j * bar_w + 8
            x2 = x1 + bar_w - 12
            draw.rounded_rectangle((x1, bottom - h, x2, bottom), radius=6, fill=color)
            val = _fr_num(values[i], 1)
            tw, _ = _text_size(draw, val, small)
            draw.text((x1 + (x2 - x1 - tw) / 2, bottom - h - 26), val, font=small, fill=NAVY)
        tw, _ = _text_size(draw, mode, body_f)
        draw.text((cx - tw / 2, bottom + 16), mode, font=body_f, fill=NAVY)

    lx = 120
    for name, _, color in series:
        draw.rounded_rectangle((lx, 700, lx + 28, 728), radius=4, fill=color)
        draw.text((lx + 38, 702), name, font=body_f, fill=NAVY)
        lx += 220

    img.save(OUT / "fig25_latences.png", "PNG")


def fig_objectifs():
    rows = [
        ("Indexation complète", 25.74, 120.0, "25,74 s", "120 s"),
        ("Recherche maximale", 0.4635, 1.0, "463,50 ms", "1 s"),
    ]

    img = Image.new("RGB", (1400, 560), BG)
    draw = ImageDraw.Draw(img)
    title_f, body_f, small = font(22, True), font(20), font(16)
    draw.text((48, 28), "Temps observés rapportés aux objectifs", font=title_f, fill=NAVY)
    draw.text((48, 64), "Barre pleine = objectif. Segment coloré = valeur mesurée.", font=small, fill=GRAY)

    left, right = 80, 1320
    y = 150
    for label, observed, target, obs_txt, tgt_txt in rows:
        ratio = min(observed / target, 1)
        draw.text((left, y), label, font=body_f, fill=NAVY)
        y += 42
        draw.rounded_rectangle((left, y, right, y + 54), radius=10, fill=LIGHT, outline=NAVY, width=1)
        filled = left + int((right - left) * ratio)
        draw.rounded_rectangle((left, y, max(filled, left + 8), y + 54), radius=10, fill=SAGE)
        draw.text((left + 16, y + 14), f"{obs_txt}  /  objectif {tgt_txt}", font=small, fill=WHITE if ratio > 0.18 else NAVY)
        y += 110

    draw.text(
        (48, 500),
        "Les deux indicateurs restent très en deçà des seuils du cahier des charges, sur 1 110 documents.",
        font=small,
        fill=GRAY,
    )
    img.save(OUT / "fig26_objectifs.png", "PNG")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig_pipeline()
    fig_architecture()
    fig_hybride()
    fig_cas_utilisation()
    fig_grille_tests()
    fig_corpus_formats()
    fig_corpus_types()
    fig_latences()
    fig_objectifs()
    print(f"Figures générées dans {OUT}")


if __name__ == "__main__":
    main()
