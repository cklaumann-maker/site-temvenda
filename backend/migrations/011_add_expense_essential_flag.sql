-- Adiciona campo is_essential em expense_items para marcar despesas como essenciais
ALTER TABLE expense_items
ADD COLUMN IF NOT EXISTS is_essential BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_expense_items_is_essential ON expense_items(is_essential);

COMMENT ON COLUMN expense_items.is_essential IS 'Indica se a despesa é essencial (folha, aluguel, fornecedores críticos, etc)';

