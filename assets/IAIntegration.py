import pprint
from dataclasses import dataclass
from PySide6.scripts.project_lib import Singleton
from openai import OpenAI

from assets.config import Config


@dataclass
class FSAction:
    type: str
    args: list[str]


def parse_output(output: str) -> tuple[list[FSAction], str]:
    """
    Parse the output from the AI model to extract actions and a summary.
    :param output: The output string from the AI model.
    :return: A tuple containing a list of FSAction and a summary string.
    """
    actions = []
    summary = ""

    # Example parsing logic (to be implemented based on actual output format)
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


# noinspection PyTypeChecker
class IAIntegration(metaclass=Singleton):
    def __init__(self):
        if not Config().get("chatgpt_api_key", None):
            raise ValueError(
                "API key for ChatGPT is not set. Please configure it in the settings."
            )
        self.client = OpenAI(api_key=Config().get("chatgpt_api_key", None))
        self.model = Config().get("ai_model", "gpt-4.1")  # Default model

    def get_audit(
        self, prompt: str, dossier: dict[str, dict]
    ) -> tuple[list[FSAction], str]:
        print("Starting audit with prompt and structure:", prompt, dossier)
        string_dossier = self.generate_str_dossier(dossier)
        print(f"Current structure:\n{string_dossier}")
        instruction = f"""
You analyze and improve a folder structure.

Output : ONE LINE. Format :
mk:path;rm:path;mv:src:dest;mvc:src:dest;me:résumé (en français)

Règles (à suivre strictement) :

Commandes autorisées : mk: (créer dossier), mv: (déplacer un dossier), mvc: (déplacer le contenu d’un dossier), rm: (supprimer dossier), me: (résumé).

Ordre obligatoire : d’abord tous les mk:, puis tous les mv: / mvc:, puis tous les rm:, enfin **me:`.

mv: et mvc: : format exact commande:source:destination (deux « : » seulement) et ne déplacent qu’un seul dossier (ou son contenu) à la fois.

Chemins complets relatifs à la racine fournis pour chaque commande.

Séparateur : le point-virgule ; sans espace avant/après.

Noms créés avec mk: : uniquement lettres, chiffres, / . ' - et espace (aucun accent, guillemet typographique ou tiret long).

Chemins source dans mv:/mvc:/rm: : peuvent contenir des accents si ces dossiers existent déjà.

Ne refais pas un mk: si le dossier existe : ignore-le silencieusement.

Pas de doublons (même commande + même chemin).

Ne supprime aucun dossier sauf si une instruction rm: est fournie.

me: doit toujours être la dernière commande, rédigée en français et résumant l’opération.

structure existant:
{string_dossier}
"""
        print(instruction)
        response = self.client.chat.completions.create(
            model=self.model,  # Use dynamic model
            messages=[
                {
                    "role": "system",
                    "content": instruction
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def get_new(self, prompt: str) -> tuple[list[FSAction], str]:
        response = self.client.chat.completions.create(
            model=self.model,  # Use dynamic model
            messages=[
                {
                    "role": "system",
                    "content": """
You generate a folder structure (no files).

Output: ONE LINE. Format: mk:folder/;mk:folder/;me:summary in French

Rules:
- Only use mk: to create folders (must end with `/`)
- Use `;` as separator (no spaces)
- No files, no duplicates, no accents, smart quotes, long dashes, or incomplete commands
- Allowed chars: letters, numbers, / . ' - , and space
- me: must be last and in French""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def generate_str_dossier(self, dossier) -> str:
        """
        Convert the dossier dictionary into a string representation.
        l=N chemin[/si dossier]
        :param dossier: Dictionary representing the file system structure.
        {"test": {"fichier.txt": None, "dossier": {"fichier2.txt": None}}}
        """
        print(dossier)
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
    pprint.pp(parse_output("mk:Images/People;mk:Images/Seasons;mk:Images/Seasons/Winter;mk:Images/Seasons/Summer;mvc:Images/Vacances:Images/People;mvc:Vacances/Winter:Images/Seasons/Winter;mvc:Vacances/Summer:Images/Seasons/Summer;rm:Images/Vacances;rm:Vacances;me:structure organisee par personnes et saisons"))
