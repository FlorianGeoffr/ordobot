import pprint
from dataclasses import dataclass
from PySide6.scripts.project_lib import Singleton
from openai import OpenAI

from assets.config import Config
from assets.load_memory_context import load_memory_context  # ← Ajouté


@dataclass
class FSAction:
    type: str
    args: list[str]


def parse_output(output: str) -> tuple[list[FSAction], str]:
    actions = []
    summary = ""
    lines = output.split(";")
    for line in lines:
        if not line.startswith("me:"):
            part = line.strip().split(":")
            action = part[0].strip()
            args = part[1:]
            if action:
                actions.append(
                    FSAction(
                        type=action, args=[arg.strip() for arg in args if arg.strip()]
                    )
                )
        else:
            summary = line.replace("me:", "").strip()
    return actions, summary


class IAIntegration(metaclass=Singleton):
    def __init__(self):
        if not Config().get("chatgpt_api_key", None):
            raise ValueError(
                "API key for ChatGPT is not set. Please configure it in the settings."
            )
        self.client = OpenAI(api_key=Config().get("chatgpt_api_key", None))
        self.model = Config().get("ai_model", "gpt-4.1")

    def get_audit(
        self, prompt: str, dossier: dict[str, dict]
    ) -> tuple[list[FSAction], str]:
        string_dossier = self.generate_str_dossier(dossier)
        memory_context = load_memory_context()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
Tu es un expert en structuration de dossiers.

{memory_context}

Structure actuelle :
{string_dossier}
""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def get_new(self, prompt: str) -> tuple[list[FSAction], str]:
        memory_context = load_memory_context()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
Tu génères une structure de dossiers (pas de fichiers).

{memory_context}
""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def generate_str_dossier(self, dossier: dict[str, dict]) -> str:
        lines = []

        def traverse(d, path=""):
            print(d, path)
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append(f"{'  ' * (len(path.split('/')) - 1)} {key}/")
                    traverse(value, f"{path}/{key}")
                else:
                    lines.append(f"{'  ' * (len(path.split('/')) - 1)} {key}")

        traverse(dossier)
        return "\n".join(lines)


if __name__ == "__main__":
    pprint.pp(
        parse_output(
            "mk:Images/People;mk:Images/Seasons;mk:Images/Seasons/Winter;mk:Images/Seasons/Summer;mvc:Images/Vacances:Images/People;mvc:Vacances/Winter:Images/Seasons/Winter;mvc:Vacances/Summer:Images/Seasons/Summer;rm:Images/Vacances;rm:Vacances;me:structure organisee par personnes et saisons"
        )
    )
