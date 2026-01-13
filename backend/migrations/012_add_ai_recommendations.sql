-- Tabela para armazenar recomendações da IA (ChatGPT)
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_period_days INTEGER NOT NULL,
    analysis_start_date DATE,
    recommendations_text TEXT NOT NULL,
    recommendations_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_recommendations_created_at ON ai_recommendations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_analysis_start_date ON ai_recommendations(analysis_start_date);

COMMENT ON TABLE ai_recommendations IS 'Histórico de recomendações geradas pela IA (ChatGPT)';
COMMENT ON COLUMN ai_recommendations.recommendations_text IS 'Texto completo das recomendações';
COMMENT ON COLUMN ai_recommendations.recommendations_json IS 'Dados estruturados das recomendações (JSON)';

