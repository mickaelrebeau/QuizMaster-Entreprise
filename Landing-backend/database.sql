-- Script d'initialisation de la base de données QuizMaster Landing
-- À exécuter sur votre base PostgreSQL Railway

-- Création de la table leads pour stocker les formulaires
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    phone VARCHAR(50),
    message TEXT,
    form_type VARCHAR(50) NOT NULL CHECK (form_type IN ('demo', 'preinscription', 'contact')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_form_type ON leads(form_type);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

-- Index composite pour éviter les doublons de préinscription
CREATE UNIQUE INDEX IF NOT EXISTS idx_leads_email_form_type 
ON leads(email, form_type) 
WHERE form_type = 'preinscription';

-- Fonction pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour mettre à jour updated_at automatiquement
CREATE TRIGGER update_leads_updated_at 
    BEFORE UPDATE ON leads 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Vue pour les statistiques
CREATE OR REPLACE VIEW leads_stats AS
SELECT 
    form_type,
    COUNT(*) as total_count,
    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '7 days') as last_7_days,
    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days') as last_30_days,
    MIN(created_at) as first_lead,
    MAX(created_at) as last_lead
FROM leads 
GROUP BY form_type;

-- Commentaires sur la table
COMMENT ON TABLE leads IS 'Table pour stocker les leads de la landing page QuizMaster';
COMMENT ON COLUMN leads.form_type IS 'Type de formulaire: demo, preinscription, contact';
COMMENT ON COLUMN leads.created_at IS 'Date de création du lead';
COMMENT ON COLUMN leads.updated_at IS 'Date de dernière modification';
