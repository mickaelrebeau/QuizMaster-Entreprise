import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate_quiz(job_description: str, company_data: str):
    prompt = f"Génère un quiz d'entretien pour ce poste : {job_description} en te basant sur : {company_data}"
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json={"prompt": prompt, "model": "llama3"})
        return response.json()