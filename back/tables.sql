DROP TABLE IF EXISTS reponses_candidats, resultats, liens_candidats, reponses, questions, quizzes, fiches_poste, "Users" CASCADE;

CREATE TABLE "Users" (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    is_rh BOOLEAN DEFAULT FALSE
);

CREATE TABLE fiches_poste (
    id SERIAL PRIMARY KEY,
    titre VARCHAR,
    description TEXT,
    entreprise VARCHAR
);

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    titre VARCHAR,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    createur_id INTEGER REFERENCES "Users"(id),
    fiche_poste_id INTEGER REFERENCES fiches_poste(id)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    texte TEXT,
    quiz_id INTEGER REFERENCES quizzes(id)
);

CREATE TABLE reponses (
    id SERIAL PRIMARY KEY,
    texte TEXT,
    question_id INTEGER REFERENCES questions(id),
    is_correct BOOLEAN DEFAULT FALSE
);

CREATE TABLE liens_candidats (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id),
    token VARCHAR NOT NULL UNIQUE,
    email VARCHAR,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resultats (
    id SERIAL PRIMARY KEY,
    lien_candidat_id INTEGER REFERENCES liens_candidats(id),
    score INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reponses_candidats (
    id SERIAL PRIMARY KEY,
    lien_candidat_id INTEGER REFERENCES liens_candidats(id),
    question_id INTEGER REFERENCES questions(id),
    reponse_id INTEGER REFERENCES reponses(id)
);