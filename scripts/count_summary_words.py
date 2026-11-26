import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "travaux"
for path in sorted(root.rglob("BILAN_JOUR_*.md")):
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r"\*\*Résumé personnel :\*\*\s*\n\n(.*?)(?=\n---)",
        text,
        flags=re.S,
    )
    print(path.name + ":")
    for i, block in enumerate(blocks, 1):
        words = len(re.findall(r"\w+", block, flags=re.UNICODE))
        print(f"  Article {i}: {words} mots")
    print()
