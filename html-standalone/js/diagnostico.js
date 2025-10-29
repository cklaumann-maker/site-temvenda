// Diagnóstico Interativo - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== helpers DOM =====
    const $ = s => document.querySelector(s);
    const val = s => { const e = $(s); return e ? e.value.trim() : ''; };
    const num = s => { const x = val(s); return x === '' ? null : Number(x); };

    // ===== navegação (scroll imediato p/ sensação de velocidade) =====
    function setProgress(n) {
        [0, 1, 2, 3, 4].forEach(i => {
            const el = $("#s" + i);
            if (el) el.classList.toggle('fill', i <= n);
        });
    }

    function showStep(n) {
        document.querySelectorAll('#tv-dx22 [data-step]').forEach(el => el.style.display = 'none');
        const el = document.querySelector(`#tv-dx22 [data-step="${n}"]`);
        if (el) el.style.display = '';
        setProgress(n);
        window.scrollTo({ top: 0, behavior: 'auto' });
    }

    function nextStep(n) { showStep(n + 1); }
    function prevStep(n) { showStep(n - 1); }

    // ===== Envio para Google Sheets (rápido e não bloqueante) =====
    const WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzkQDJtruY92BHZGRaRnNSzi6FPGXAGi9-Y30UV0oNfBEsmuZkgZYBOGT4fggwzdLrvCA/exec";
    
    function enviarParaSheets(payload) {
        try {
            if (!WEB_APP_URL) return;
            const body = JSON.stringify(payload);

            // 1) Tenta sendBeacon (não bloqueia a UI e funciona bem com text/plain)
            if (navigator.sendBeacon) {
                const ok = navigator.sendBeacon(WEB_APP_URL, new Blob([body], { type: 'text/plain' }));
                if (ok) return;
            }

            // 2) Fallback: fetch no-cors com text/plain (evita preflight CORS)
            fetch(WEB_APP_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
                body,
                keepalive: true
            }).catch(() => {});
        } catch (_e) {}
    }

    // ===== valida lead (etapa 0) — AVANÇA IMEDIATO =====
    window.validarLeadEProsseguir = function() {
        const nome = val('#lead_nome');
        const emp = val('#lead_empresa');
        const tel = val('#lead_tel');
        const email = val('#lead_email');
        const emailOK = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

        if (!nome || !emp || !tel || !emailOK) {
            let faltando = [];
            if (!nome) faltando.push('Nome');
            if (!emp) faltando.push('Empresa');
            if (!tel) faltando.push('Telefone');
            if (!emailOK) faltando.push('E-mail válido');
            alert('Preencha: ' + faltando.join(', ') + '.');
            return;
        }

        const btn = $('#btn_start');
        if (btn) {
            btn.disabled = true;
            btn.style.opacity = .85;
            btn.style.cursor = 'default';
            btn.setAttribute('aria-busy', 'true');
        }

        // AVANÇA JÁ (não espera rede)
        nextStep(0);

        // dispara envio em background
        enviarParaSheets({ etapa: 'lead', lead: { nome, empresa: emp, tel, email } });

        if (btn) {
            setTimeout(() => {
                btn.disabled = false;
                btn.style.opacity = '';
                btn.style.cursor = '';
                btn.removeAttribute('aria-busy');
            }, 300);
        }
    };

    // ===== mostrar/ocultar campos condicionais =====
    function toggleWrap(selectId, expected, wrapId) {
        const sel = $(selectId), wrap = $(wrapId);
        function sync() {
            if (!sel || !wrap) return;
            wrap.style.display = (sel.value === expected) ? '' : 'none';
        }
        if (sel) {
            sel.addEventListener('change', sync);
            sync();
        }
    }

    // Comercial metas
    toggleWrap('#gc_orcamento', 'sim', '#gc_orcamento_val_wrap');
    toggleWrap('#gc_meta_margem', 'sim', '#gc_meta_margem_val_wrap');

    // Financeiro: CMV alvo e ajuda
    (function() {
        const sel = $('#gf_cmv_meta'), wrap = $('#gf_cmv_val_wrap'), help = $('#gf_cmv_help');
        function sync() {
            if (!sel) return;
            if (wrap) wrap.style.display = (sel.value === 'sim') ? '' : 'none';
            if (help) help.style.display = (sel.value === 'nao') ? '' : 'none';
        }
        if (sel) {
            sel.addEventListener('change', sync);
            sync();
        }
    })();

    // Ciclo financeiro alvo e ajuda
    (function() {
        const sel = $('#gf_ciclo_meta'), wrap = $('#gf_ciclo_val_wrap'), help = $('#gf_ciclo_help');
        function sync() {
            if (!sel) return;
            if (wrap) wrap.style.display = (sel.value === 'sim') ? '' : 'none';
            if (help) help.style.display = (sel.value === 'nao') ? '' : 'none';
        }
        if (sel) {
            sel.addEventListener('change', sync);
            sync();
        }
    })();

    // Caixa negativo → necessidade de caixa
    toggleWrap('#gf_caixa_pos', 'nao', '#gf_caixa_need_wrap');

    // Giro de estoque
    (function() {
        const sel = $('#gf_giro_sabe');
        const wrap = $('#gf_giro_val_wrap');
        const help = $('#gf_giro_help');
        function sync() {
            if (!sel) return;
            if (wrap) wrap.style.display = (sel.value === 'sim') ? '' : 'none';
            if (help) help.style.display = (sel.value === 'nao') ? '' : 'none';
        }
        if (sel) {
            sel.addEventListener('change', sync);
            sync();
        }
    })();

    // NPS: nota quando "sim", explicação quando "nao"
    (function() {
        const sel = $('#go_nps_aplica'), wrap = $('#go_nps_val_wrap'), help = $('#go_nps_help');
        function sync() {
            if (!sel) return;
            if (wrap) wrap.style.display = (sel.value === 'sim') ? '' : 'none';
            if (help) help.style.display = (sel.value === 'nao') ? '' : 'none';
        }
        if (sel) {
            sel.addEventListener('change', sync);
            sync();
        }
    })();

    // ===== % tipos devem somar 100 =====
    function validarTipos100() {
        const gen = Number(val('#gc_p_gen') || 0),
            prop = Number(val('#gc_p_prop') || 0),
            perf = Number(val('#gc_p_perf') || 0);
        const soma = gen + prop + perf, err = $('#sumErr');
        if (Math.abs(soma - 100) > 0.001) {
            if (err) {
                err.style.display = 'block';
                err.textContent = `A soma precisa ser 100%. Agora: ${soma.toFixed(1)}%`;
            }
            return false;
        }
        if (err) err.style.display = 'none';
        return true;
    }
    ['#gc_p_gen', '#gc_p_prop', '#gc_p_perf'].forEach(q => {
        const e = $(q);
        if (e) e.addEventListener('input', validarTipos100);
    });

    // ===== calcula % margem automaticamente =====
    function syncMargemPct() {
        const vendas = Number(val('#gc_vendas_atuais') || 0);
        const mVal = Number(val('#gc_margem_valor') || 0);
        const pct = (vendas > 0 && mVal >= 0) ? (mVal / vendas * 100) : null;
        $('#gc_margem_pct_calc').textContent = (pct !== null) ? (pct.toFixed(2).replace('.', ',') + ' %') : '— %';
    }
    ['#gc_vendas_atuais', '#gc_margem_valor'].forEach(q => {
        const e = $(q);
        if (e) e.addEventListener('input', syncMargemPct);
    });

    window.validarComercialENext = function() {
        if (!validarTipos100()) {
            alert('A composição por tipo (Genérico/Similar, Propagado, Perfumaria) precisa somar 100%.');
            return;
        }
        nextStep(1);
    };

    // ===== scores simples =====
    const tagByScore = s => (s >= 75 ? { txt: 'Saudável', cls: 'ok' } : s >= 50 ? { txt: 'Atenção', cls: 'warn' } : { txt: 'Risco', cls: 'risk' });

    function scoreFinanceiro({ cmv, ciclo, caixaPos, giro, dre, fluxo }) {
        let s = 0;
        if (cmv !== null) {
            if (cmv < 65) s += 35;
            else if (cmv <= 75) s += 25;
            else s += 10;
        } else s += 20;
        if (typeof ciclo === 'number') {
            s += (ciclo < 0) ? 25 : 15;
        } else s += 20;
        s += (caixaPos === 'sim') ? 20 : 8;
        if (typeof giro === 'number') {
            s += (giro >= 10) ? 20 : (giro >= 6 ? 15 : 8);
        } else s += 12;
        s += (dre === 'sim') ? 10 : 4;
        s += (fluxo === 'sim') ? 10 : 4;
        return Math.min(100, Math.round(s));
    }

    function scoreComercial({ ticket, itens, gen, prop, perf, orc, metaMargem, campanhas }) {
        let s = 0;
        if (ticket >= 60) s += 18;
        else if (ticket >= 40) s += 12;
        else s += 7;
        if (itens >= 2) s += 18;
        else if (itens >= 1.5) s += 12;
        else s += 7;
        if (gen > 35) s += 12;
        else if (gen >= 20) s += 9;
        else s += 5;
        if (prop >= 20) s += 8;
        else s += 5;
        if (perf >= 10) s += 8;
        else s += 5;
        s += (orc === 'sim') ? 12 : 6;
        s += (metaMargem === 'sim') ? 12 : 6;
        s += (campanhas === 'sim') ? 12 : 6;
        return Math.min(100, Math.round(s));
    }

    function scoreOps({ checklist, nps, rituais, padrao }) {
        let s = 0;
        s += (checklist === 'sim') ? 25 : 10;
        s += (typeof nps === 'number') ? Math.min(35, nps * 3.5) : 18;
        if (rituais === 'diaria_semanal_mensal') s += 30;
        else if (rituais === 'diaria_semanal') s += 22;
        else if (rituais === 'diaria') s += 16;
        else s += 8;
        s += (padrao === 'sim') ? 20 : 10;
        return Math.min(100, Math.round(s));
    }

    // ===== relatório =====
    window.gerarRelatorio = function() {
        const interesseConsultoria = val('#gn_q_consultoria');
        const interesseFormacao = val('#gn_q_formacao');
        if (!interesseConsultoria || !interesseFormacao) {
            alert('Responda às duas perguntas finais (consultoria e contato para Formação).');
            showStep(4);
            return;
        }

        const lead = { nome: val('#lead_nome'), empresa: val('#lead_empresa'), tel: val('#lead_tel'), email: val('#lead_email') };

        const vendas = Number(val('#gc_vendas_atuais') || 0);
        const margemValor = Number(val('#gc_margem_valor') || 0);
        const margemPctCalc = vendas > 0 ? (margemValor / vendas * 100) : null;

        const gc = {
            orc: val('#gc_orcamento'),
            orcVal: num('#gc_orcamento_val'),
            metaMargem: val('#gc_meta_margem'),
            metaMargemVal: num('#gc_meta_margem_val'),
            vendasAtuais: vendas,
            margemValor,
            margemPctCalc,
            campanhas: val('#gc_campanhas'),
            ticket: num('#gc_ticket') || 0,
            itens: num('#gc_itens_cupom') || 0,
            gen: num('#gc_p_gen') || 0,
            prop: num('#gc_p_prop') || 0,
            perf: num('#gc_p_perf') || 0,
            mix: num('#gc_mix') || 0,
        };

        if (!validarTipos100()) {
            alert('A composição por tipo precisa fechar 100%.');
            showStep(1);
            return;
        }

        const gf = {
            cmvMeta: val('#gf_cmv_meta'),
            cmvAtual: num('#gf_cmv_atual'),
            cmvVal: num('#gf_cmv_val'),
            cicloMeta: val('#gf_ciclo_meta'),
            cicloAtual: (val('#gf_ciclo_atual') !== '' ? num('#gf_ciclo_atual') : null),
            cicloVal: (val('#gf_ciclo_val') !== '' ? num('#gf_ciclo_val') : null),
            caixaPos: val('#gf_caixa_pos'),
            caixaNeed: num('#gf_caixa_need'),
            giroSabe: val('#gf_giro_sabe'),
            giroVal: num('#gf_giro_val'),
            dre: val('#gf_dre'),
            fluxo: val('#gf_fluxo')
        };

        const go = {
            checklist: val('#go_checklist'),
            npsAplica: val('#go_nps_aplica'),
            npsVal: (val('#go_nps_val') !== '' ? num('#go_nps_val') : null),
            rituais: val('#go_rituais'),
            padrao: val('#go_padrao')
        };
        const lojas = num('#gn_lojas') || 1, colab = num('#gn_colab') || 1;
        const gn = { lojas, colab, processos: val('#gn_processos') };

        const margemPorColab = (colab > 0) ? (margemValor / colab) : 0;
        const vendaMediaPorLoja = (lojas > 0) ? (vendas / lojas) : 0;

        const valorGen = vendas * (gc.gen || 0) / 100;
        const valorProp = vendas * (gc.prop || 0) / 100;
        const valorPerf = vendas * (gc.perf || 0) / 100;

        const finScore = scoreFinanceiro({
            cmv: (gf.cmvAtual !== null ? gf.cmvAtual : null),
            ciclo: (gf.cicloAtual !== null ? gf.cicloAtual : null),
            caixaPos: gf.caixaPos,
            giro: (gf.giroVal !== null ? gf.giroVal : null),
            dre: gf.dre,
            fluxo: gf.fluxo
        });
        const comScore = scoreComercial({
            ticket: gc.ticket, itens: gc.itens, gen: gc.gen, prop: gc.prop, perf: gc.perf,
            orc: gc.orc, metaMargem: gc.metaMargem, campanhas: gc.campanhas
        });
        const opsScore = scoreOps({
            checklist: go.checklist, nps: (go.npsAplica === 'sim' ? go.npsVal : null), rituais: go.rituais, padrao: go.padrao
        });
        const finTag = tagByScore(finScore), comTag = tagByScore(comScore), opsTag = tagByScore(opsScore);

        $('#k_fin').textContent = finScore + '/100';
        $('#k_fin').className = 'val ' + finTag.cls;
        $('#k_ops').textContent = opsScore + '/100';
        $('#k_ops').className = 'val ' + opsTag.cls;
        $('#k_com').textContent = comScore + '/100';
        $('#k_com').className = 'val ' + comTag.cls;
        $('#t_fin').textContent = finTag.txt;
        $('#t_ops').textContent = opsTag.txt;
        $('#t_com').textContent = comTag.txt;

        const explicacoes = [
            (gc.orc !== 'sim') && '• Sem orçamento: defina metas mensais por loja/categoria.',
            (gc.metaMargem !== 'sim') && '• Sem meta de margem: estabeleça % alvo por categoria e monitore semanalmente.',
            (gc.campanhas !== 'sim') && '• Crie calendário mensal de campanhas (ticket/penetração).',
            (gf.cmvMeta !== 'sim') && '• CMV: calcule (CMV/Vendas)×100. Saudável <65%; 65–75% estável; >75% ruim.',
            '• Ciclo financeiro: quanto menor, melhor — o dinheiro sai e volta mais rápido, gerando mais caixa.',
            (gf.caixaPos === 'nao') && '• Caixa negativo: reduza estoque, renegocie prazos e acelere recebíveis.',
            (gf.giroSabe !== 'sim') && '• Giro: CMV ÷ Estoque Médio. Limpe itens parados, aumente mix vencedor.',
            (gf.dre !== 'sim') && '• Estruture DRE mensal para decisões de preço e despesas.',
            (gf.fluxo !== 'sim') && '• Projete fluxo de caixa 13 semanas.',
            (go.checklist !== 'sim') && '• Padronize checklist de abertura/fechamento, PDV, estoque, preços.',
            (go.npsAplica !== 'sim') && '• Aplique NPS mensalmente (0–10) e aja sobre feedbacks.',
            (go.rituais === 'nao') && '• Implante rituais: 15', semanal e fechamento mensal.',
            (go.padrao !== 'sim') && '• Roteiro de balcão: abordagem → escuta ativa → recomendação → fechamento.'
        ].filter(Boolean);

        const resumo =
            `DADOS DO CONTATO
- Nome: ${lead.nome}
- Empresa: ${lead.empresa}
- Telefone: ${lead.tel}
- E-mail: ${lead.email}

RESUMO EXECUTIVO
- Financeiro: ${finScore}/100 (${finTag.txt}) • Operação/Pessoas: ${opsScore}/100 (${opsTag.txt}) • Comercial: ${comScore}/100 (${comTag.txt})

GESTÃO COMERCIAL
- Orçamento: ${gc.orc}${gc.orc === 'sim' && gc.orcVal ? ' • R$ ' + gc.orcVal.toLocaleString('pt-BR') : ''}
- Meta de margem: ${gc.metaMargem}${gc.metaMargem === 'sim' && gc.metaMargemVal ? ' • ' + gc.metaMargemVal + '%' : ''}
- Vendas atuais (todas as lojas): R$ ${vendas.toLocaleString('pt-BR')}
- Margem atual: R$ ${margemValor.toLocaleString('pt-BR')}${margemPctCalc !== null ? ' (' + margemPctCalc.toFixed(2).replace('.', ',') + '%)' : ''}
- Mix de vendas: Genérico/Similar ${gc.gen}%, Propagado ${gc.prop}%, Perfumaria ${gc.perf}% (soma 100%)

VALOR POR TIPO DE PRODUTO (R$)
- Genérico/Similar: R$ ${valorGen.toFixed(2).toString().replace('.', ',')}
- Propagado: R$ ${valorProp.toFixed(2).toString().replace('.', ',')}
- Perfumaria: R$ ${valorPerf.toFixed(2).toString().replace('.', ',')}

- Ticket médio: R$ ${gc.ticket != null ? gc.ticket.toLocaleString('pt-BR') : '—'}
- Itens/cupom: ${gc.itens}
- Campanhas de vendas: ${gc.campanhas || '—'}
- Itens no mix: ${gc.mix || '—'}

GESTÃO FINANCEIRA
- CMV meta: ${gf.cmvMeta || '—'} • CMV atual: ${gf.cmvAtual !== null ? gf.cmvAtual + '%' : '—'}${gf.cmvMeta === 'sim' && gf.cmvVal !== null ? ' • alvo ' + gf.cmvVal + '%' : ''}
- Ciclo financeiro: ${gf.cicloAtual !== null ? gf.cicloAtual + ' dias (atual)' : '—'}${gf.cicloMeta === 'sim' && gf.cicloVal !== null ? ' • alvo ' + gf.cicloVal + ' dias' : ''}
- Caixa positivo: ${gf.caixaPos || '—'}${gf.caixaPos === 'nao' && gf.caixaNeed ? ' • Necessidade R$ ' + gf.caixaNeed.toLocaleString('pt-BR') : ''}
- Giro de estoque: ${gf.giroSabe || '—'}${gf.giroVal !== null ? ' • ' + gf.giroVal + 'x/ano' : ''}
- DRE: ${gf.dre || '—'} • Fluxo de caixa: ${gf.fluxo || '—'}

GESTÃO DA OPERAÇÃO
- Checklist: ${go.checklist || '—'} • NPS aplica: ${go.npsAplica || '—'}${go.npsAplica === 'sim' && go.npsVal !== null ? ' • Nota ' + go.npsVal + '/10' : ''}
- Rituais: ${go.rituais || '—'} • Padrão de atendimento: ${go.padrao || '—'}

GESTÃO DO NEGÓCIO
- Lojas: ${lojas} • Colaboradores: ${colab} • Processos: ${gn.processos || '—'}

INTERESSE EM SOLUÇÕES TEM VENDA
- Conhecer consultoria: ${interesseConsultoria}
- Contato para Formação Líderes de Farmácia: ${interesseFormacao}

INDICADORES DERIVADOS
- Vendas médias por loja: R$ ${vendaMediaPorLoja ? vendaMediaPorLoja.toFixed(2).toString().replace('.', ',') : '—'}
- Produtividade por colaborador (vendas/colab): R$ ${colab ? (vendas / colab).toFixed(2).toString().replace('.', ',') : '—'}
- Margem por colaborador (margem/colab): R$ ${colab ? margemPorColab.toFixed(2).toString().replace('.', ',') : '—'}
- CMV saudável: <65% • Estável: 65–75% • Ruim: >75%
- Ciclo financeiro: quanto menor, melhor (dinheiro sai e volta mais rápido → gera mais caixa).

PONTOS DE ATENÇÃO E SUGESTÕES
${explicacoes.length ? explicacoes.join('\n') : '• Boa disciplina geral. Próximo passo: ganhos finos em mix, pricing e rituais.'}
`;

        $('#report').textContent = resumo;
        $('#resultado').style.display = '';

        const prioridades = explicacoes.slice(0, 3).join(' ');
        const resumoPrint =
            `TEM VENDA — RESUMO DO DIAGNÓSTICO
Empresa: ${lead.empresa} • Contato: ${lead.nome} • Tel: ${lead.tel} • E-mail: ${lead.email}

SCORES
• Financeiro: ${finScore}/100 (${finTag.txt}) | Operação: ${opsScore}/100 (${opsTag.txt}) | Comercial: ${comScore}/100 (${comTag.txt})

NÚMEROS-CHAVE
• Vendas: R$ ${vendas.toLocaleString('pt-BR')} | Margem: R$ ${margemValor.toLocaleString('pt-BR')}${margemPctCalc !== null ? ' (' + margemPctCalc.toFixed(1).replace('.', ',') + '%)' : ''}
• Mix: Gen/Sim ${gc.gen}% | Prop ${gc.prop}% | Perf ${gc.perf}%
• Ticket: R$ ${gc.ticket != null ? gc.ticket.toLocaleString('pt-BR') : '—'} | Itens/Cupom: ${gc.itens}
• CMV: ${gf.cmvAtual != null ? gf.cmvAtual + '%' : '—'} | Ciclo: ${gf.cicloAtual != null ? gf.cicloAtual + ' d' : '—'} | Giro: ${gf.giroVal != null ? gf.giroVal + 'x/ano' : '—'}

DERIVADOS
• Venda/Loja: R$ ${vendaMediaPorLoja ? vendaMediaPorLoja.toFixed(2).toString().replace('.', ',') : '—'}
• Margem/Colab: R$ ${colab ? (margemPorColab).toFixed(2).toString().replace('.', ',') : '—'}

INTERESSES
• Consultoria: ${interesseConsultoria} | Formação Líderes: ${interesseFormacao}

PRÓXIMAS 3 PRIORIDADES
${prioridades || '• Consolidar rituais, mix e pricing para elevar margem e giro.'}
`;
        $('#resumo_print').textContent = resumoPrint;

        const msg = encodeURIComponent("Diagnóstico • TEM VENDA\n\n" + resumo + "\nQuero um plano de 90 dias.");
        $('#whats_btn').href = "https://wa.me/5548991575566?text=" + msg;
        const assunto = encodeURIComponent("Diagnóstico TEM VENDA - " + lead.empresa);
        $('#mail_btn').href = "mailto:" + lead.email + "?subject=" + assunto + "&body=" + encodeURIComponent(resumo);

        enviarParaSheets({
            etapa: 'final',
            lead, gc, gf, go, gn,
            interesseConsultoria,
            interesseFormacao,
            vendaMediaPorLoja,
            produtividadeColab: (colab ? (vendas / colab) : 0),
            margemPorColab,
            valorGen, valorProp, valorPerf,
            finScore, comScore, opsScore,
            resumo, resumoPrint
        });

        window.scrollTo({ top: $('#resultado').offsetTop - 10, behavior: 'auto' });
    };

    window.copiarRelatorio = function() {
        const txt = $('#report').textContent;
        navigator.clipboard.writeText(txt).then(() => alert('Relatório copiado!')).catch(() => alert('Não foi possível copiar.'));
    };

    // Funções globais para navegação
    window.nextStep = nextStep;
    window.prevStep = prevStep;

    // init
    showStep(0);
});
