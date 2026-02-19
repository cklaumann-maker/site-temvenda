// CNPJ Upload Manager - Gerencia upload de CNPJs via CSV/Excel
// Feira Digital Farma

class CNPJUploadManager {
    constructor(supabase) {
        this.supabase = supabase;
    }

    async parseCSV(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const text = e.target.result;
                    const lines = text.split('\n').filter(line => line.trim());
                    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
                    
                    const data = [];
                    for (let i = 1; i < lines.length; i++) {
                        const values = this.parseCSVLine(lines[i]);
                        if (values.length >= 2) {
                            const row = {};
                            headers.forEach((header, index) => {
                                row[header] = values[index]?.trim() || '';
                            });
                            data.push(row);
                        }
                    }
                    resolve(data);
                } catch (error) {
                    reject(error);
                }
            };
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }
        result.push(current);
        return result;
    }

    async parseExcel(file) {
        // Para Excel, precisaríamos de uma biblioteca como SheetJS
        // Por enquanto, retornar erro pedindo CSV
        throw new Error('Por favor, converta o arquivo Excel para CSV antes de fazer o upload.');
    }

    async uploadCNPJs(data) {
        try {
            // Validar e formatar CNPJs
            const cnpjs = data.map(row => {
                let cnpj = (row.cnpj || row.CNPJ || '').replace(/\D/g, '');
                if (cnpj.length !== 14) {
                    throw new Error(`CNPJ inválido: ${cnpj} (deve ter 14 dígitos)`);
                }

                return {
                    cnpj: cnpj,
                    razao_social: row.razao_social || row['razão social'] || row['Razão Social'] || '',
                    nome_fantasia: row.nome_fantasia || row['nome fantasia'] || row['Nome Fantasia'] || '',
                    ativo: true
                };
            });

            // Inserir em lote
            const { data: result, error } = await this.supabase
                .from('fdf_cnpjs_base')
                .upsert(cnpjs, { onConflict: 'cnpj' });

            if (error) throw error;

            return {
                success: true,
                count: cnpjs.length,
                message: `${cnpjs.length} CNPJs processados com sucesso!`
            };
        } catch (error) {
            console.error('Erro ao fazer upload de CNPJs:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    createUploadInterface(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="data-table" style="margin-bottom: 24px;">
                <div class="table-header">
                    <h2 class="table-title">Upload de CNPJs</h2>
                </div>
                <div style="padding: 24px;">
                    <div class="form-group">
                        <label class="form-label">Arquivo CSV *</label>
                        <input type="file" id="cnpjFileInput" accept=".csv,.txt" class="form-input">
                        <div style="margin-top: 8px; color: var(--fdf-white-medium); font-size: 12px;">
                            Formato esperado: CSV com colunas: CNPJ, Razão Social, Nome Fantasia (opcional)
                        </div>
                    </div>
                    <div id="cnpjUploadPreview" style="margin-top: 16px;"></div>
                    <div class="form-actions" style="margin-top: 24px; padding-top: 0; border-top: none;">
                        <button class="btn-primary" onclick="window.cnpjUploadManager.handleUpload()">
                            📤 Fazer Upload
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Preview do arquivo
        document.getElementById('cnpjFileInput').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const preview = document.getElementById('cnpjUploadPreview');
                preview.innerHTML = `
                    <div style="color: var(--fdf-green); font-size: 14px;">
                        ✅ Arquivo selecionado: ${file.name} (${(file.size / 1024).toFixed(2)} KB)
                    </div>
                `;
            }
        });
    }

    async handleUpload() {
        const fileInput = document.getElementById('cnpjFileInput');
        const file = fileInput?.files[0];
        
        if (!file) {
            alert('Por favor, selecione um arquivo CSV.');
            return;
        }

        try {
            const preview = document.getElementById('cnpjUploadPreview');
            preview.innerHTML = '<div style="color: var(--fdf-white-medium);">Processando...</div>';

            const data = await this.parseCSV(file);
            const result = await this.uploadCNPJs(data);

            if (result.success) {
                preview.innerHTML = `
                    <div style="color: var(--fdf-green); font-size: 14px; padding: 16px; background: rgba(94, 225, 0, 0.1); border-radius: 8px; border: 1px solid rgba(94, 225, 0, 0.3);">
                        ✅ ${result.message}
                    </div>
                `;
                fileInput.value = '';
                
                // Recarregar dados se CRUD Manager estiver ativo
                if (window.crudManager && window.crudManager.entityType === 'cnpjs') {
                    await window.crudManager.loadData();
                }
            } else {
                preview.innerHTML = `
                    <div style="color: #ff4d4d; font-size: 14px; padding: 16px; background: rgba(255, 77, 77, 0.1); border-radius: 8px; border: 1px solid rgba(255, 77, 77, 0.3);">
                        ❌ Erro: ${result.error}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Erro no upload:', error);
            const preview = document.getElementById('cnpjUploadPreview');
            preview.innerHTML = `
                <div style="color: #ff4d4d; font-size: 14px; padding: 16px; background: rgba(255, 77, 77, 0.1); border-radius: 8px; border: 1px solid rgba(255, 77, 77, 0.3);">
                    ❌ Erro: ${error.message}
                </div>
            `;
        }
    }
}
