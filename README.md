# QuizMaster-Entreprise

## Description
QuizMaster-Entreprise est une plateforme de génération de quiz d'entretien d'embauche par IA, adaptée aux besoins des entreprises. L'IA (Ollama) s'entraîne sur les données internes et génère des quiz personnalisés selon les fiches de poste.

- **Frontend** : Vue 3, Tailwind, shadcn-vue
- **Backend** : FastAPI, PostgreSQL
- **IA** : Ollama (hébergée localement)

## Structure du projet

```
QuizMaster-Entreprise/
│
├── back/         # Backend FastAPI
├── front/        # Frontend Vue 3
└── README.md
```

## Lancer le backend

1. Installer les dépendances :
   ```bash
   cd back
   pip install -r requirements.txt
   ```
2. Configurer la base PostgreSQL (voir DATABASE_URL dans back/database.py)
3. Lancer le serveur :
   ```bash
   uvicorn main:app --reload
   ```

## Lancer le frontend

1. Installer les dépendances :
   ```bash
   cd front
   npm install
   ```
2. Lancer le serveur de dev :
   ```bash
   npm run dev
   ```

## Lancer Ollama (IA locale)

1. Installer Ollama : https://ollama.com/
2. Démarrer le serveur Ollama avec le modèle souhaité (ex : llama3)

## Fonctionnalités principales
- Création de fiches de poste
- Génération de quiz par IA
- Envoi de liens aux candidats
- Réponse aux quiz côté candidat
- Visualisation des résultats pour les RH

---

Pour toute question, voir la documentation dans chaque dossier ou contacter l'équipe technique.