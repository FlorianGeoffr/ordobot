from assets.config import Config

models_ollama = {
    "TinyLlama": {
        "name": "tinyllama",
        "description": "Ultra-léger, utile pour tests simples"
    },
    "Deepseek Coder 1.3B": {
        "name": "deepseek-coder:1.3b",
        "description": "Léger, bon en JSON mais limité sur prompts complexes"
    },
    "Deepseek Coder 6.7B": {
        "name": "deepseek-coder:6.7b",
        "description": "Très bon en génération de JSON structuré, idéal pour ce projet"
    },
    "Mistral 7B Instruct": {
        "name": "mistral",
        "description": "Bon équilibre, instructions bien comprises, efficace en JSON"
    },
    "LLaMA2 7B": {
        "name": "llama2",
        "description": "Modèle généraliste stable, nécessite un prompt bien cadré"
    },
    "LLaMA3 8B Instruct": {
        "name": "llama3",
        "description": "Très bon sur prompts flous, bonne compréhension du contexte"
    },
    "Mixtral 12.7B": {
        "name": "mixtral",
        "description": "Modèle puissant et lourd, adapté à des demandes longues ou complexes"
    }
}

class ModeleIA:

    @staticmethod
    def get_model_name():
        return Config().get("model_ia", "Deepseek Coder 6.7B")

    @staticmethod
    def get_ollama_name():
        model = ModeleIA.get_model_name()
        if model in models_ollama:
            return models_ollama[model]["name"]
        else:
            raise ValueError(f"Modèle '{model}' non reconnu. Choisissez parmi : {list(models_ollama.keys())}")

    @staticmethod
    def set_model(model):
        if model in models_ollama:
            Config().set("model_ia", model)
        else:
            raise ValueError(f"Modèle '{model}' non reconnu. Choisissez parmi : {list(models_ollama.keys())}")

    @staticmethod
    def get_description_model(model):
        if model in models_ollama:
            return models_ollama[model]["description"]
        else:
            raise ValueError(f"Modèle '{model}' non reconnu. Choisissez parmi : {list(models_ollama.keys())}")

    @staticmethod
    def list_models():
        return list(models_ollama.keys())