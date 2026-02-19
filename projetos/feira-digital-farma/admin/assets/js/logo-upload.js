// Logo Upload Manager - Gerencia upload de logos para parceiros
// Feira Digital Farma

class LogoUploadManager {
    constructor(supabase) {
        this.supabase = supabase;
        this.bucketName = 'fdf-logos';
        this.maxSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    }

    async uploadLogo(file, partnerId, partnerType) {
        try {
            // Validar arquivo
            this.validateFile(file);

            // Gerar nome único
            const fileExt = file.name.split('.').pop();
            const fileName = `${partnerType}_${partnerId}_${Date.now()}.${fileExt}`;
            const filePath = `${partnerType}/${fileName}`;

            // Upload para Supabase Storage
            const { data, error } = await this.supabase.storage
                .from(this.bucketName)
                .upload(filePath, file, {
                    cacheControl: '3600',
                    upsert: false
                });

            if (error) throw error;

            // Obter URL pública
            const { data: urlData } = this.supabase.storage
                .from(this.bucketName)
                .getPublicUrl(filePath);

            return {
                success: true,
                url: urlData.publicUrl,
                path: filePath
            };
        } catch (error) {
            console.error('Erro no upload:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    validateFile(file) {
        // Validar tipo
        if (!this.allowedTypes.includes(file.type)) {
            throw new Error('Formato inválido. Use PNG ou JPG.');
        }

        // Validar tamanho
        if (file.size > this.maxSize) {
            throw new Error(`Arquivo muito grande. Tamanho máximo: ${this.maxSize / 1024 / 1024}MB`);
        }
    }

    async deleteLogo(filePath) {
        try {
            const { error } = await this.supabase.storage
                .from(this.bucketName)
                .remove([filePath]);

            if (error) throw error;
            return { success: true };
        } catch (error) {
            console.error('Erro ao deletar logo:', error);
            return { success: false, error: error.message };
        }
    }

    createPreviewElement(file, containerId) {
        return new Promise((resolve) => {
            const container = document.getElementById(containerId);
            if (!container) {
                resolve(null);
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const previewHTML = `
                    <div class="logo-preview" style="margin-top: 16px;">
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <img src="${e.target.result}" 
                                 alt="Preview" 
                                 style="max-width: 200px; max-height: 200px; border-radius: 8px; border: 1px solid var(--fdf-glass-border);">
                            <div>
                                <div style="color: var(--fdf-white-medium); font-size: 14px; margin-bottom: 4px;">
                                    ${file.name}
                                </div>
                                <div style="color: var(--fdf-white-light); font-size: 12px;">
                                    ${(file.size / 1024).toFixed(2)} KB
                                </div>
                                <div style="color: var(--fdf-green); font-size: 12px; margin-top: 8px;">
                                    ✅ Tamanho recomendado: 300x300px (PNG ou JPG, máx. 5MB)
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML = previewHTML;
                resolve(e.target.result);
            };
            reader.readAsDataURL(file);
        });
    }
}
