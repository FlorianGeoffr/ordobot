import json
from pathlib import Path

def load_memory_context() -> str:
    with open(Path("assets/memory.json"), "r", encoding="utf-8") as f:
        memory = json.load(f)

    def format_list(label, items):
        return f"{label}:\n" + "\n".join(f"- {item}" for item in items)

    sections = [
        format_list("Objectifs", memory.get("objectifs", [])),
        format_list("Contraintes", memory.get("contraintes", [])),
        format_list("Actions disponibles", memory.get("actions_disponibles", [])),
        format_list("Exemples", memory.get("exemples", [])),
        "Format de sortie attendu:\n" + memory.get("format_sortie", {}).get("structure", "")
    ]
    return "\n\n".join(sections)
