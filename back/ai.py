import httpx
import asyncio
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:27b"

async def generate_quiz(job_description: str, company_data: str):
    prompt = f"Génère un quiz d'entretien pour ce poste : {job_description} en te basant sur : {company_data}"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            # On active le stream
            async with client.stream("POST", OLLAMA_URL, json=payload, headers=headers, timeout=120) as response:
                response.raise_for_status()
                full_message = ""
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    # Chaque ligne est un JSON
                    data = json.loads(line)
                    # Pour debug
                    # print("Chunk Ollama :", data)
                    # On assemble le message
                    if "message" in data and "content" in data["message"]:
                        full_message += data["message"]["content"]
                if not full_message:
                    raise ValueError("Aucune réponse utile reçue d'Ollama.")
                
                print(full_message)
                return {"message": full_message}
        except Exception as e:
            print("Erreur lors de l'appel à Ollama :", e)
            return {"error": str(e)}

# Placeholder pour l'entraînement du modèle sur des données d'entreprise
async def train_model_on_company_data(company_id: int, data: str):
    # Ici, tu pourrais appeler une API Ollama ou un script pour fine-tuner le modèle
    # sur les données de l'entreprise. À implémenter selon les possibilités d'Ollama.
    # Par exemple :
    # await client.post("http://localhost:11434/api/train", json={...})
    pass


if __name__ == "__main__":
    job_description = """Fiche de Poste – Développeur Vue.js (H/F)

📍 Localisation : Télétravail / Reims
🕒 Type de contrat : CDI / CDD / Alternance / Freelance
📅 Disponibilité : Dès que possible
💼 Expérience requise : 1 an minimum (alternance et stages inclus)

À propos de QuizMaster

Chez QuizMaster, nous révolutionnons le recrutement. Grâce à notre plateforme propulsée par l'intelligence artificielle, nous générons des quiz sur mesure pour aider les recruteurs à évaluer efficacement les candidats lors des entretiens. Notre mission : rendre le recrutement plus objectif, plus rapide et plus pertinent.
Missions

En tant que Développeur Vue.js, tu seras au cœur du développement de notre interface utilisateur. Tes missions principales incluront :

    Développer et améliorer notre application front-end en Vue.js 3 (composition API).

    Collaborer avec l'équipe produit et les designers pour créer une interface utilisateur fluide et intuitive.

    Intégrer les appels aux API d'IA (OpenAI, Hugging Face, Ollama, etc.) pour générer dynamiquement les contenus.

    Participer aux choix techniques et à l'amélioration continue du code.

    Corriger les bugs et optimiser les performances de l'application.

Profil recherché

    Tu as au moins 1 an d'expérience en développement front-end (alternance et stages inclus).

    Tu maîtrises Vue.js (idéalement Vue 3 et Composition API).

    Tu es à l'aise avec HTML, CSS (ou TailwindCSS), JavaScript (ES6+).

    Tu comprends le fonctionnement des API REST/GraphQL.

    Tu es curieux(se), rigoureux(se), et tu aimes travailler en équipe.

    Une appétence pour les technologies IA est un plus !

Ce que nous offrons

    Un environnement startup dynamique et bienveillant.

    Des responsabilités réelles dès le début.

    La possibilité de contribuer à un produit innovant à fort impact.

    Télétravail flexible / hybride possible.

    Participation à des meetups et conférences tech.

Tu veux créer des outils utiles, simples, et dopés à l'IA ?
📩 Envoie-nous ton CV (et quelques projets si tu en as) à [adresse email].
📍 Plus d'infos sur nous : [site web ou LinkedIn de l'entreprise]"""

    asyncio.run(generate_quiz(job_description, "QuizMaster Entreprise, une entreprise de génération de quiz sur mesure pour le recrutement."))
