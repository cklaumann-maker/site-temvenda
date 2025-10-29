<?php
/*
Template Name: Diagnóstico TemVenda
Template Post Type: page
*/
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnóstico TemVenda - <?php bloginfo('name'); ?></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Moderno */
        .header {
            background: linear-gradient(135deg, #5ee100 0%, #4bc800 100%);
            color: #000000;
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(94, 225, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }

        .header p {
            font-size: 1.3rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        /* Progress Bar Moderna */
        .progress-container {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .progress-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #5ee100;
        }

        .progress-percentage {
            font-size: 1.1rem;
            color: #5ee100;
            font-weight: 700;
            background: rgba(94, 225, 0, 0.2);
            padding: 8px 15px;
            border-radius: 20px;
        }

        .progress-bar {
            width: 100%;
            height: 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #5ee100, #94ff3b);
            border-radius: 10px;
            transition: width 0.8s ease;
            position: relative;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Steps Indicators */
        .steps {
            display: flex;
            justify-content: space-between;
            gap: 10px;
        }

        .step {
            text-align: center;
            flex: 1;
            position: relative;
        }

        .step::after {
            content: '';
            position: absolute;
            top: 25px;
            left: 50%;
            right: -50%;
            height: 3px;
            background: rgba(255,255,255,0.2);
            z-index: 0;
        }

        .step:last-child::after {
            display: none;
        }

        .step.completed::after,
        .step.active::after {
            background: #5ee100;
        }

        .step-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-weight: bold;
            font-size: 18px;
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
            border: 3px solid transparent;
        }

        .step.active .step-circle {
            background: #5ee100;
            color: #000;
            transform: scale(1.1);
            border-color: #94ff3b;
            box-shadow: 0 0 20px rgba(94, 225, 0, 0.5);
        }

        .step.completed .step-circle {
            background: #5ee100;
            color: #000;
            border-color: #94ff3b;
        }

        .step.completed .step-circle::before {
            content: '✓';
            font-size: 20px;
        }

        .step-label {
            font-size: 14px;
            font-weight: 600;
            opacity: 0.7;
            color: #b2b2b2;
        }

        .step.active .step-label {
            opacity: 1;
            color: #5ee100;
        }

        .step.completed .step-label {
            opacity: 1;
            color: #5ee100;
        }

        /* Cards Modernos */
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: none;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #5ee100, #94ff3b);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .card.active {
            display: block;
        }

        .card.active::before {
            opacity: 1;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: rgba(94, 225, 0, 0.3);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .card h2 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 30px;
            color: #5ee100;
            text-align: center;
        }

        /* Form Elements Modernos */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .form-group {
            position: relative;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 12px;
            color: #ffffff;
            font-size: 16px;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 18px 20px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            color: #ffffff;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: inherit;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #5ee100;
            background: rgba(94, 225, 0, 0.05);
            box-shadow: 0 0 0 4px rgba(94, 225, 0, 0.1);
            transform: translateY(-2px);
        }

        .form-group input::placeholder {
            color: rgba(255,255,255,0.5);
        }

        .form-group small {
            display: block;
            margin-top: 8px;
            font-size: 14px;
            color: #b2b2b2;
        }

        /* Help Boxes Modernos */
        .help-box {
            background: rgba(94, 225, 0, 0.1);
            border: 2px solid rgba(94, 225, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            font-size: 15px;
            line-height: 1.6;
            display: none;
            animation: slideDown 0.3s ease;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .help-box.show {
            display: block;
        }

        .help-box strong {
            color: #5ee100;
            font-size: 16px;
            display: block;
            margin-bottom: 10px;
        }

        /* Botões Modernos */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 18px 30px;
            border-radius: 15px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            border: none;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            min-width: 150px;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn-primary {
            background: linear-gradient(135deg, #5ee100, #4bc800);
            color: #000000;
            box-shadow: 0 5px 15px rgba(94, 225, 0, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(94, 225, 0, 0.4);
        }

        .btn-secondary {
            background: transparent;
            color: #ffffff;
            border: 2px solid rgba(255,255,255,0.3);
        }

        .btn-secondary:hover {
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-2px);
        }

        .btn-group {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 40px;
            flex-wrap: wrap;
        }

        /* Results Modernos */
        .results {
            background: linear-gradient(135deg, rgba(94, 225, 0, 0.1), rgba(148, 255, 59, 0.1));
            border: 2px solid rgba(94, 225, 0, 0.3);
            border-radius: 25px;
            padding: 40px;
            margin-top: 40px;
            display: none;
            animation: fadeInUp 0.5s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .kpis {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .kpi {
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease;
        }

        .kpi:hover {
            transform: translateY(-5px);
        }

        .kpi-title {
            font-size: 14px;
            color: #b2b2b2;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .kpi-value {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .kpi-status {
            font-size: 16px;
            font-weight: 600;
        }

        .kpi.ok .kpi-value { color: #84ff6a; }
        .kpi.warn .kpi-value { color: #ffd86a; }
        .kpi.risk .kpi-value { color: #ff7a7a; }

        .report {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            border-radius: 20px;
            padding: 0;
            margin: 25px 0;
            border: 1px solid rgba(255,255,255,0.2);
            overflow: hidden;
        }

        .report-header {
            background: linear-gradient(135deg, #5ee100, #4bc800);
            color: #000;
            padding: 25px;
            text-align: center;
        }

        .report-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .report-subtitle {
            font-size: 1.1rem;
            opacity: 0.8;
        }

        .report-content {
            padding: 30px;
        }

        .report-section {
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            border-left: 4px solid #5ee100;
        }

        .report-section h3 {
            color: #5ee100;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .report-section h4 {
            color: #fff;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 15px 0 8px 0;
        }

        .report-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .report-item:last-child {
            border-bottom: none;
        }

        .report-label {
            color: #b2b2b2;
            font-weight: 500;
        }

        .report-value {
            color: #fff;
            font-weight: 600;
        }

        .score-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
        }

        .score-ok {
            background: rgba(132, 255, 106, 0.2);
            color: #84ff6a;
            border: 1px solid rgba(132, 255, 106, 0.3);
        }

        .score-warn {
            background: rgba(255, 216, 106, 0.2);
            color: #ffd86a;
            border: 1px solid rgba(255, 216, 106, 0.3);
        }

        .score-risk {
            background: rgba(255, 122, 122, 0.2);
            color: #ff7a7a;
            border: 1px solid rgba(255, 122, 122, 0.3);
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .summary-card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .summary-card h4 {
            color: #5ee100;
            font-size: 1rem;
            margin-bottom: 10px;
        }

        .summary-card .value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
        }

        .summary-card .label {
            font-size: 0.9rem;
            color: #b2b2b2;
            margin-top: 5px;
        }

        .recommendations {
            background: rgba(94, 225, 0, 0.1);
            border: 1px solid rgba(94, 225, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }

        .recommendations h4 {
            color: #5ee100;
            font-size: 1.2rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .recommendation-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }

        .recommendation-item:last-child {
            margin-bottom: 0;
        }

        .recommendation-icon {
            color: #5ee100;
            font-weight: bold;
            margin-top: 2px;
        }

        .contact-info {
            background: linear-gradient(135deg, rgba(94, 225, 0, 0.1), rgba(148, 255, 59, 0.1));
            border: 2px solid rgba(94, 225, 0, 0.3);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            margin-top: 30px;
        }

        .contact-info h4 {
            color: #5ee100;
            font-size: 1.3rem;
            margin-bottom: 15px;
        }

        .contact-item {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin: 10px 0;
            color: #fff;
        }

        .contact-item a {
            color: #5ee100;
            text-decoration: none;
            font-weight: 600;
        }

        .contact-item a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .report-content {
                padding: 20px;
            }
            
            .summary-grid {
                grid-template-columns: 1fr;
            }
            
            .report-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }
        }

        /* Step Indicator */
        .step-indicator {
            text-align: center;
            margin-bottom: 30px;
            font-size: 20px;
            font-weight: 700;
            color: #5ee100;
            background: rgba(94, 225, 0, 0.1);
            padding: 15px;
            border-radius: 15px;
            border: 1px solid rgba(94, 225, 0, 0.3);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }

            .header h1 {
                font-size: 2.2rem;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .btn-group {
                flex-direction: column;
                align-items: center;
            }

            .btn {
                width: 100%;
                max-width: 300px;
            }

            .steps {
                flex-wrap: wrap;
                gap: 15px;
            }

            .step {
                flex: 0 0 calc(50% - 7.5px);
            }

            .kpis {
                grid-template-columns: 1fr;
            }

            .card {
                padding: 25px;
            }

            .card h2 {
                font-size: 1.8rem;
            }
        }

        /* Loading Animation */
        .loading {
            position: relative;
            pointer-events: none;
        }

        .loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            margin: -10px 0 0 -10px;
            border: 2px solid transparent;
            border-top-color: currentColor;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Print styles */
        @media print {
            body {
                background: #fff;
                color: #000;
            }
            
            .header {
                background: #5ee100;
                color: #000;
            }
            
            .card {
                background: #fff;
                border: 1px solid #ddd;
                color: #000;
            }
            
            .btn-group {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Diagnóstico TemVenda</h1>
            <p>Como está sua empresa hoje?</p>
        </div>

        <!-- Progress -->
        <div class="progress-container">
            <div class="progress-header">
                <span class="progress-title">Progresso do Diagnóstico</span>
                <span class="progress-percentage" id="progress-percentage">20%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 20%"></div>
            </div>
            <div class="steps">
                <div class="step active" data-step="0">
                    <div class="step-circle">1</div>
                    <div class="step-label">Dados</div>
                </div>
                <div class="step" data-step="1">
                    <div class="step-circle">2</div>
                    <div class="step-label">Comercial</div>
                </div>
                <div class="step" data-step="2">
                    <div class="step-circle">3</div>
                    <div class="step-label">Financeiro</div>
                </div>
                <div class="step" data-step="3">
                    <div class="step-circle">4</div>
                    <div class="step-label">Operação</div>
                </div>
                <div class="step" data-step="4">
                    <div class="step-circle">5</div>
                    <div class="step-label">Negócio</div>
                </div>
            </div>
        </div>

        <div class="step-indicator" id="step-indicator">Etapa 1 de 5 - Seus dados pessoais</div>

        <form id="formDX">
            <!-- ETAPA 0 — Lead -->
            <div class="card active" id="card-0">
                <h2>📋 Seus dados pessoais</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Nome completo *</label>
                        <input id="lead_nome" required placeholder="Digite seu nome completo" />
                    </div>
                    <div class="form-group">
                        <label>Empresa *</label>
                        <input id="lead_empresa" required placeholder="Nome da sua empresa" />
                    </div>
                    <div class="form-group">
                        <label>Telefone (WhatsApp) *</label>
                        <input id="lead_tel" required placeholder="(DD) 90000-0000" />
                    </div>
                    <div class="form-group">
                        <label>E-mail *</label>
                        <input id="lead_email" type="email" required placeholder="seu@email.com.br" />
                    </div>
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-primary" onclick="validarLeadEProsseguir()">
                        🚀 Começar diagnóstico
                    </button>
                </div>
            </div>

            <!-- ETAPA 1 — Comercial -->
            <div class="card" id="card-1">
                <h2>💰 Gestão Comercial</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Possui orçamento de vendas?</label>
                        <select id="gc_orcamento" onchange="toggleHelp('gc_orcamento', 'gc_orcamento_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="nao">Não</option>
                            <option value="sim">Sim</option>
                        </select>
                        <div id="gc_orcamento_help" class="help-box">
                            <strong>O que é orçamento de vendas?</strong>
                            É o planejamento financeiro que define quanto a empresa espera vender em um período (mensal, trimestral, anual). Serve como meta e referência para acompanhar o desempenho real versus o planejado.
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Vendas atuais (todas as lojas) — R$</label>
                        <input type="number" id="gc_vendas_atuais" min="0" step="0.01" placeholder="Exemplo: 320.000" />
                        <small>Digite o valor total de vendas de todas as suas lojas</small>
                    </div>

                    <div class="form-group">
                        <label>Possui campanhas de vendas?</label>
                        <select id="gc_campanhas" onchange="toggleHelp('gc_campanhas', 'gc_campanhas_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="nao">Não</option>
                            <option value="sim">Sim</option>
                        </select>
                        <div id="gc_campanhas_help" class="help-box">
                            <strong>O que são campanhas de vendas?</strong>
                            São ações promocionais planejadas para aumentar vendas, como descontos, promoções, lançamentos de produtos, datas comemorativas, etc. Ajudam a impulsionar resultados e criar sazonalidade positiva.
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Ticket médio (R$)</label>
                        <input type="number" id="gc_ticket" min="0" step="0.01" placeholder="Exemplo: 62,50" />
                        <small>Valor médio por venda</small>
                    </div>
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-secondary" onclick="prevStep(1)">← Voltar</button>
                    <button type="button" class="btn btn-primary" onclick="nextStep(1)">Próximo →</button>
                </div>
            </div>

            <!-- ETAPA 2 — Financeiro -->
            <div class="card" id="card-2">
                <h2>💳 Gestão Financeira</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Possui meta de CMV?</label>
                        <select id="gf_cmv_meta" onchange="toggleHelp('gf_cmv_meta', 'gf_cmv_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="nao">Não</option>
                            <option value="sim">Sim</option>
                        </select>
                        <div id="gf_cmv_help" class="help-box">
                            <strong>O que é CMV?</strong>
                            CMV (Custo da Mercadoria Vendida) é o valor gasto para adquirir os produtos que foram vendidos.<br><br>
                            <strong>Como calcular CMV em %:</strong> (CMV ÷ Vendas) × 100<br>
                            <strong>Exemplo:</strong> Se CMV = R$ 70.000 e Vendas = R$ 100.000, então CMV = 70%<br><br>
                            <strong>Referências:</strong><br>
                            • <strong>Saudável:</strong> abaixo de 65%<br>
                            • <strong>Estável:</strong> entre 65% e 75%<br>
                            • <strong>Ruim:</strong> acima de 75%
                        </div>
                    </div>

                    <div class="form-group">
                        <label>CMV atual (%)</label>
                        <input type="number" id="gf_cmv_atual" min="0" max="100" step="0.1" placeholder="Exemplo: 70" />
                        <small>Percentual atual do CMV</small>
                    </div>

                    <div class="form-group">
                        <label>Seu caixa está positivo?</label>
                        <select id="gf_caixa_pos">
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Possui DRE?</label>
                        <select id="gf_dre" onchange="toggleHelp('gf_dre', 'gf_dre_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                        <div id="gf_dre_help" class="help-box">
                            <strong>O que é DRE?</strong>
                            DRE (Demonstração do Resultado do Exercício) é um relatório que mostra se a empresa teve lucro ou prejuízo em um período.<br><br>
                            <strong>Estrutura básica:</strong><br>
                            • Receita Bruta<br>
                            • (-) Impostos sobre vendas<br>
                            • (=) Receita Líquida<br>
                            • (-) CMV<br>
                            • (=) Lucro Bruto<br>
                            • (-) Despesas Operacionais<br>
                            • (=) Lucro Operacional<br><br>
                            <strong>Importância:</strong> Ajuda a tomar decisões sobre preços, despesas e investimentos.
                        </div>
                    </div>
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-secondary" onclick="prevStep(2)">← Voltar</button>
                    <button type="button" class="btn btn-primary" onclick="nextStep(2)">Próximo →</button>
                </div>
            </div>

            <!-- ETAPA 3 — Operação -->
            <div class="card" id="card-3">
                <h2>⚙️ Gestão da Operação</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Checklist de operação?</label>
                        <select id="go_checklist" onchange="toggleHelp('go_checklist', 'go_checklist_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                        <div id="go_checklist_help" class="help-box">
                            <strong>O que é checklist de operação?</strong>
                            São listas de verificação para padronizar processos diários, semanais e mensais.<br><br>
                            <strong>Exemplos de checklist:</strong><br>
                            • <strong>Abertura:</strong> conferir caixa, ligar equipamentos, verificar preços<br>
                            • <strong>Durante o dia:</strong> manter estoque organizado, limpeza, atendimento<br>
                            • <strong>Fechamento:</strong> conferir vendas, fechar caixa, organizar estoque<br><br>
                            <strong>Benefícios:</strong> Reduz erros, melhora qualidade e aumenta produtividade.
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Aplica NPS?</label>
                        <select id="go_nps_aplica" onchange="toggleHelp('go_nps_aplica', 'go_nps_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="nao">Não</option>
                            <option value="sim">Sim</option>
                        </select>
                        <div id="go_nps_help" class="help-box">
                            <strong>O que é NPS?</strong>
                            NPS (Net Promoter Score) mede a probabilidade de o cliente indicar sua empresa para outros (escala de 0 a 10).<br><br>
                            <strong>Como aplicar:</strong><br>
                            • Pergunta: "De 0 a 10, qual a probabilidade de você indicar nossa empresa?"<br>
                            • <strong>Promotores:</strong> 9-10 (clientes satisfeitos)<br>
                            • <strong>Neutros:</strong> 7-8 (clientes satisfeitos)<br>
                            • <strong>Detratores:</strong> 0-6 (clientes insatisfeitos)<br><br>
                            <strong>Cálculo:</strong> % Promotores - % Detratores = NPS<br>
                            <strong>Meta:</strong> NPS acima de 50 é considerado excelente.
                        </div>
                    </div>

                    <div class="form-group">
                        <label>NPS atual (0-10)</label>
                        <input type="number" id="go_nps_val" min="0" max="10" step="0.1" placeholder="Exemplo: 8,6" />
                        <small>Nota média dos clientes</small>
                    </div>

                    <div class="form-group">
                        <label>Padrão de atendimento?</label>
                        <select id="go_padrao" onchange="toggleHelp('go_padrao', 'go_padrao_help')">
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                        <div id="go_padrao_help" class="help-box">
                            <strong>O que é padrão de atendimento?</strong>
                            É um roteiro padronizado para o atendimento ao cliente, garantindo qualidade e consistência.<br><br>
                            <strong>Roteiro básico:</strong><br>
                            1. <strong>Abordagem:</strong> Cumprimentar com sorriso<br>
                            2. <strong>Escuta ativa:</strong> Entender a necessidade do cliente<br>
                            3. <strong>Recomendação:</strong> Sugerir produtos adequados<br>
                            4. <strong>Fechamento:</strong> Confirmar a compra<br>
                            5. <strong>Pós-venda:</strong> Orientar sobre uso e garantia<br><br>
                            <strong>Benefícios:</strong> Aumenta satisfação do cliente e vendas.
                        </div>
                    </div>
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-secondary" onclick="prevStep(3)">← Voltar</button>
                    <button type="button" class="btn btn-primary" onclick="nextStep(3)">Próximo →</button>
                </div>
            </div>

            <!-- ETAPA 4 — Negócio -->
            <div class="card" id="card-4">
                <h2>🏢 Gestão do Negócio</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Quantidade de lojas</label>
                        <input type="number" id="gn_lojas" min="1" step="1" placeholder="Exemplo: 1" />
                        <small>Número total de lojas</small>
                    </div>
                    <div class="form-group">
                        <label>Quantidade de colaboradores</label>
                        <input type="number" id="gn_colab" min="1" step="1" placeholder="Exemplo: 12" />
                        <small>Número total de funcionários</small>
                    </div>
                </div>

                <div class="help-box" style="display: block; background: rgba(94, 225, 0, 0.15);">
                    <strong>Perguntas finais importantes:</strong><br>
                    Suas respostas nos ajudarão a personalizar melhor nossa proposta de trabalho.
                </div>

                <div class="form-grid">
                    <div class="form-group">
                        <label>Você gostaria de conhecer nosso trabalho de consultoria?</label>
                        <select id="gn_q_consultoria" required>
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Você gostaria que eu contatasse seu time para apresentar a Formação Líderes de Farmácia?</label>
                        <select id="gn_q_formacao" required>
                            <option value="">Selecione uma opção</option>
                            <option value="sim">Sim</option>
                            <option value="nao">Não</option>
                        </select>
                    </div>
                </div>

                <div class="btn-group">
                    <button type="button" class="btn btn-secondary" onclick="prevStep(4)">← Voltar</button>
                    <button type="button" class="btn btn-primary" onclick="gerarRelatorio()">🎯 Gerar relatório</button>
                </div>
            </div>
        </form>

        <!-- RESULTADO -->
        <div id="resultado" class="results">
            <h2>📊 Seu diagnóstico completo</h2>
            <div class="kpis">
                <div class="kpi" id="kpi-fin">
                    <div class="kpi-title">Financeiro</div>
                    <div class="kpi-value" id="k_fin">–</div>
                    <div class="kpi-status" id="t_fin"></div>
                </div>
                <div class="kpi" id="kpi-ops">
                    <div class="kpi-title">Operação</div>
                    <div class="kpi-value" id="k_ops">–</div>
                    <div class="kpi-status" id="t_ops"></div>
                </div>
                <div class="kpi" id="kpi-com">
                    <div class="kpi-title">Comercial</div>
                    <div class="kpi-value" id="k_com">–</div>
                    <div class="kpi-status" id="t_com"></div>
                </div>
            </div>
            <div class="report" id="report"></div>
            <div class="btn-group">
                <button class="btn btn-secondary" onclick="copiarRelatorio()">📋 Copiar</button>
                <button class="btn btn-secondary" onclick="window.print()">🖨️ Imprimir</button>
                <a id="whats_btn" class="btn btn-primary" href="#" target="_blank">📱 WhatsApp</a>
                <a id="mail_btn" class="btn btn-secondary" href="#" target="_blank">📧 E-mail</a>
            </div>
        </div>
    </div>

    <script>
        let currentStep = 0;
        const totalSteps = 5;

        // Atualizar indicador de etapa
        function updateStepIndicator(step) {
            const stepNames = [
                'Etapa 1 de 5 - Seus dados pessoais',
                'Etapa 2 de 5 - Gestão Comercial',
                'Etapa 3 de 5 - Gestão Financeira',
                'Etapa 4 de 5 - Gestão da Operação',
                'Etapa 5 de 5 - Gestão do Negócio'
            ];
            document.getElementById('step-indicator').textContent = stepNames[step];
        }

        // Sistema de Progresso
        function updateProgress(step) {
            const percentage = ((step + 1) / totalSteps) * 100;
            document.getElementById('progress-percentage').textContent = Math.round(percentage) + '%';
            document.getElementById('progress-fill').style.width = percentage + '%';
            
            // Atualizar steps
            document.querySelectorAll('.step').forEach((stepEl, index) => {
                stepEl.classList.remove('active', 'completed');
                if (index < step) {
                    stepEl.classList.add('completed');
                } else if (index === step) {
                    stepEl.classList.add('active');
                }
            });
        }

        // Navegação
        function showStep(n) {
            // Esconder todos os cards
            for (let i = 0; i < totalSteps; i++) {
                const card = document.getElementById('card-' + i);
                if (card) {
                    card.classList.remove('active');
                    card.style.display = 'none';
                }
            }
            
            // Mostrar card atual
            const currentCard = document.getElementById('card-' + n);
            if (currentCard) {
                currentCard.style.display = 'block';
                currentCard.classList.add('active');
            }
            
            currentStep = n;
            updateStepIndicator(n);
            updateProgress(n);
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        function nextStep(n) { 
            showStep(n + 1); 
        }
        
        function prevStep(n) { 
            showStep(n - 1); 
        }

        // Validação Lead
        function validarLeadEProsseguir() {
            const nome = document.getElementById('lead_nome').value.trim();
            const empresa = document.getElementById('lead_empresa').value.trim();
            const tel = document.getElementById('lead_tel').value.trim();
            const email = document.getElementById('lead_email').value.trim();
            
            if (!nome || !empresa || !tel || !email) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }
            
            nextStep(0);
        }

        // Sistema de Help Boxes
        function toggleHelp(selectId, helpId) {
            const select = document.getElementById(selectId);
            const help = document.getElementById(helpId);
            
            if (select && help) {
                if (select.value === 'nao') {
                    help.classList.add('show');
                } else {
                    help.classList.remove('show');
                }
            }
        }

        // Sistema de Scores
        function scoreFinanceiro({cmv, caixaPos, dre}) {
            let s = 0;
            if (cmv !== null) {
                if (cmv < 65) s += 40;
                else if (cmv <= 75) s += 30;
                else s += 15;
            } else s += 25;
            
            s += (caixaPos === 'sim') ? 30 : 10;
            s += (dre === 'sim') ? 30 : 15;
            
            return Math.min(100, Math.round(s));
        }

        function scoreComercial({orc, campanhas}) {
            let s = 50; // Base
            s += (orc === 'sim') ? 25 : 10;
            s += (campanhas === 'sim') ? 25 : 10;
            return Math.min(100, Math.round(s));
        }

        function scoreOps({checklist, nps, padrao}) {
            let s = 50; // Base
            s += (checklist === 'sim') ? 20 : 10;
            s += (typeof nps === 'number') ? Math.min(20, nps * 2) : 15;
            s += (padrao === 'sim') ? 20 : 10;
            return Math.min(100, Math.round(s));
        }

        const tagByScore = s => (s >= 75 ? {txt: 'Saudável', cls: 'ok'} : s >= 50 ? {txt: 'Atenção', cls: 'warn'} : {txt: 'Risco', cls: 'risk'});

        // Geração de Relatório
        function gerarRelatorio() {
            const interesseConsultoria = document.getElementById('gn_q_consultoria').value;
            const interesseFormacao = document.getElementById('gn_q_formacao').value;
            
            if (!interesseConsultoria || !interesseFormacao) {
                alert('Por favor, responda às duas perguntas finais.');
                showStep(4);
                return;
            }

            const lead = {
                nome: document.getElementById('lead_nome').value,
                empresa: document.getElementById('lead_empresa').value,
                tel: document.getElementById('lead_tel').value,
                email: document.getElementById('lead_email').value
            };

            const vendas = Number(document.getElementById('gc_vendas_atuais').value || 0);

            const gc = {
                orc: document.getElementById('gc_orcamento').value,
                vendasAtuais: vendas,
                campanhas: document.getElementById('gc_campanhas').value,
                ticket: Number(document.getElementById('gc_ticket').value || 0)
            };

            const gf = {
                cmvMeta: document.getElementById('gf_cmv_meta').value,
                cmvAtual: Number(document.getElementById('gf_cmv_atual').value || 0),
                caixaPos: document.getElementById('gf_caixa_pos').value,
                dre: document.getElementById('gf_dre').value
            };

            const go = {
                checklist: document.getElementById('go_checklist').value,
                npsVal: Number(document.getElementById('go_nps_val').value || 0),
                padrao: document.getElementById('go_padrao').value
            };

            const lojas = Number(document.getElementById('gn_lojas').value || 1);
            const colab = Number(document.getElementById('gn_colab').value || 1);

            const finScore = scoreFinanceiro({
                cmv: gf.cmvAtual || null,
                caixaPos: gf.caixaPos,
                dre: gf.dre
            });

            const comScore = scoreComercial({
                orc: gc.orc,
                campanhas: gc.campanhas
            });

            const opsScore = scoreOps({
                checklist: go.checklist,
                nps: go.npsVal || null,
                padrao: go.padrao
            });

            const finTag = tagByScore(finScore);
            const comTag = tagByScore(comScore);
            const opsTag = tagByScore(opsScore);

            // Atualizar KPIs
            document.getElementById('k_fin').textContent = finScore + '/100';
            document.getElementById('k_fin').className = 'kpi-value ' + finTag.cls;
            document.getElementById('t_fin').textContent = finTag.txt;

            document.getElementById('k_ops').textContent = opsScore + '/100';
            document.getElementById('k_ops').className = 'kpi-value ' + opsTag.cls;
            document.getElementById('t_ops').textContent = opsTag.txt;

            document.getElementById('k_com').textContent = comScore + '/100';
            document.getElementById('k_com').className = 'kpi-value ' + comTag.cls;
            document.getElementById('t_com').textContent = comTag.txt;

            // Atualizar classes dos KPIs
            document.getElementById('kpi-fin').className = 'kpi ' + finTag.cls;
            document.getElementById('kpi-ops').className = 'kpi ' + opsTag.cls;
            document.getElementById('kpi-com').className = 'kpi ' + comTag.cls;

            // Gerar recomendações baseadas nos scores
            const recomendacoes = [];
            if (finScore < 50) {
                recomendacoes.push('Implementar controle rigoroso de CMV e fluxo de caixa');
                recomendacoes.push('Estruturar DRE mensal para tomada de decisões');
            }
            if (comScore < 50) {
                recomendacoes.push('Criar orçamento de vendas mensal por categoria');
                recomendacoes.push('Desenvolver calendário de campanhas promocionais');
            }
            if (opsScore < 50) {
                recomendacoes.push('Implementar checklist de operação diário');
                recomendacoes.push('Aplicar NPS mensalmente para medir satisfação');
                recomendacoes.push('Padronizar processo de atendimento ao cliente');
            }
            if (recomendacoes.length === 0) {
                recomendacoes.push('Manter disciplina atual e focar em melhorias incrementais');
                recomendacoes.push('Implementar rituais de gestão semanais e mensais');
            }

            const resumo = `
                <div class="report-header">
                    <div class="report-title">📊 Relatório de Diagnóstico</div>
                    <div class="report-subtitle">${lead.empresa} • ${new Date().toLocaleDateString('pt-BR')}</div>
                </div>
                <div class="report-content">
                    <div class="report-section">
                        <h3>👤 Dados do Contato</h3>
                        <div class="summary-grid">
                            <div class="summary-card">
                                <h4>Nome</h4>
                                <div class="value">${lead.nome}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Empresa</h4>
                                <div class="value">${lead.empresa}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Telefone</h4>
                                <div class="value">${lead.tel}</div>
                            </div>
                            <div class="summary-card">
                                <h4>E-mail</h4>
                                <div class="value">${lead.email}</div>
                            </div>
                        </div>
                    </div>

                    <div class="report-section">
                        <h3>📈 Resumo Executivo</h3>
                        <div class="summary-grid">
                            <div class="summary-card">
                                <h4>Financeiro</h4>
                                <div class="value">${finScore}/100</div>
                                <div class="label score-badge ${finTag.cls}">${finTag.txt}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Operação</h4>
                                <div class="value">${opsScore}/100</div>
                                <div class="label score-badge ${opsTag.cls}">${opsTag.txt}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Comercial</h4>
                                <div class="value">${comScore}/100</div>
                                <div class="label score-badge ${comTag.cls}">${comTag.txt}</div>
                            </div>
                        </div>
                    </div>

                    <div class="report-section">
                        <h3>💰 Gestão Comercial</h3>
                        <div class="report-item">
                            <span class="report-label">Orçamento de vendas</span>
                            <span class="report-value">${gc.orc === 'sim' ? '✅ Sim' : gc.orc === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Vendas atuais</span>
                            <span class="report-value">R$ ${vendas.toLocaleString('pt-BR')}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Ticket médio</span>
                            <span class="report-value">R$ ${gc.ticket ? gc.ticket.toLocaleString('pt-BR') : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Campanhas de vendas</span>
                            <span class="report-value">${gc.campanhas === 'sim' ? '✅ Sim' : gc.campanhas === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                    </div>

                    <div class="report-section">
                        <h3>💳 Gestão Financeira</h3>
                        <div class="report-item">
                            <span class="report-label">Meta de CMV</span>
                            <span class="report-value">${gf.cmvMeta === 'sim' ? '✅ Sim' : gf.cmvMeta === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">CMV atual</span>
                            <span class="report-value">${gf.cmvAtual ? gf.cmvAtual + '%' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Caixa positivo</span>
                            <span class="report-value">${gf.caixaPos === 'sim' ? '✅ Sim' : gf.caixaPos === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">DRE estruturada</span>
                            <span class="report-value">${gf.dre === 'sim' ? '✅ Sim' : gf.dre === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                    </div>

                    <div class="report-section">
                        <h3>⚙️ Gestão da Operação</h3>
                        <div class="report-item">
                            <span class="report-label">Checklist de operação</span>
                            <span class="report-value">${go.checklist === 'sim' ? '✅ Sim' : go.checklist === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">NPS atual</span>
                            <span class="report-value">${go.npsVal ? go.npsVal + '/10' : '—'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Padrão de atendimento</span>
                            <span class="report-value">${go.padrao === 'sim' ? '✅ Sim' : go.padrao === 'nao' ? '❌ Não' : '—'}</span>
                        </div>
                    </div>

                    <div class="report-section">
                        <h3>🏢 Gestão do Negócio</h3>
                        <div class="summary-grid">
                            <div class="summary-card">
                                <h4>Lojas</h4>
                                <div class="value">${lojas}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Colaboradores</h4>
                                <div class="value">${colab}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Vendas por loja</h4>
                                <div class="value">R$ ${lojas > 0 ? (vendas/lojas).toLocaleString('pt-BR') : '—'}</div>
                            </div>
                            <div class="summary-card">
                                <h4>Produtividade</h4>
                                <div class="value">R$ ${colab > 0 ? (vendas/colab).toLocaleString('pt-BR') : '—'}</div>
                            </div>
                        </div>
                    </div>

                    <div class="recommendations">
                        <h4>💡 Recomendações Prioritárias</h4>
                        ${recomendacoes.map(rec => `
                            <div class="recommendation-item">
                                <span class="recommendation-icon">•</span>
                                <span>${rec}</span>
                            </div>
                        `).join('')}
                    </div>

                    <div class="report-section">
                        <h3>🎯 Interesse em Soluções TemVenda</h3>
                        <div class="report-item">
                            <span class="report-label">Consultoria</span>
                            <span class="report-value">${interesseConsultoria === 'sim' ? '✅ Sim' : '❌ Não'}</span>
                        </div>
                        <div class="report-item">
                            <span class="report-label">Formação Líderes</span>
                            <span class="report-value">${interesseFormacao === 'sim' ? '✅ Sim' : '❌ Não'}</span>
                        </div>
                    </div>

                    <div class="contact-info">
                        <h4>📞 Próximos Passos</h4>
                        <div class="contact-item">
                            <span>📱 WhatsApp:</span>
                            <a href="https://wa.me/5548991575566" target="_blank">(48) 99157-5566</a>
                        </div>
                        <div class="contact-item">
                            <span>📧 E-mail:</span>
                            <a href="mailto:contato@temvenda.com.br">contato@temvenda.com.br</a>
                        </div>
                        <p style="margin-top: 15px; color: #b2b2b2; font-size: 14px;">
                            Entre em contato para um plano personalizado de 90 dias
                        </p>
                    </div>
                </div>
            `;

            document.getElementById('report').innerHTML = resumo;
            document.getElementById('resultado').style.display = 'block';

            // Criar versão de texto simples para WhatsApp
            const textoSimples = `📊 DIAGNÓSTICO TEM VENDA

👤 DADOS DO CONTATO
• Nome: ${lead.nome}
• Empresa: ${lead.empresa}
• Telefone: ${lead.tel}
• E-mail: ${lead.email}

📈 RESUMO EXECUTIVO
• Financeiro: ${finScore}/100 (${finTag.txt})
• Operação: ${opsScore}/100 (${opsTag.txt})
• Comercial: ${comScore}/100 (${comTag.txt})

💰 GESTÃO COMERCIAL
• Orçamento: ${gc.orc === 'sim' ? '✅ Sim' : gc.orc === 'nao' ? '❌ Não' : '—'}
• Vendas atuais: R$ ${vendas.toLocaleString('pt-BR')}
• Ticket médio: R$ ${gc.ticket ? gc.ticket.toLocaleString('pt-BR') : '—'}
• Campanhas: ${gc.campanhas === 'sim' ? '✅ Sim' : gc.campanhas === 'nao' ? '❌ Não' : '—'}

💳 GESTÃO FINANCEIRA
• CMV meta: ${gf.cmvMeta === 'sim' ? '✅ Sim' : gf.cmvMeta === 'nao' ? '❌ Não' : '—'}
• CMV atual: ${gf.cmvAtual ? gf.cmvAtual + '%' : '—'}
• Caixa positivo: ${gf.caixaPos === 'sim' ? '✅ Sim' : gf.caixaPos === 'nao' ? '❌ Não' : '—'}
• DRE: ${gf.dre === 'sim' ? '✅ Sim' : gf.dre === 'nao' ? '❌ Não' : '—'}

⚙️ GESTÃO DA OPERAÇÃO
• Checklist: ${go.checklist === 'sim' ? '✅ Sim' : go.checklist === 'nao' ? '❌ Não' : '—'}
• NPS atual: ${go.npsVal ? go.npsVal + '/10' : '—'}
• Padrão de atendimento: ${go.padrao === 'sim' ? '✅ Sim' : go.padrao === 'nao' ? '❌ Não' : '—'}

🏢 GESTÃO DO NEGÓCIO
• Lojas: ${lojas}
• Colaboradores: ${colab}
• Vendas por loja: R$ ${lojas > 0 ? (vendas/lojas).toLocaleString('pt-BR') : '—'}
• Produtividade: R$ ${colab > 0 ? (vendas/colab).toLocaleString('pt-BR') : '—'}

💡 RECOMENDAÇÕES PRIORITÁRIAS
${recomendacoes.map(rec => `• ${rec}`).join('\n')}

🎯 INTERESSE EM SOLUÇÕES TEM VENDA
• Consultoria: ${interesseConsultoria === 'sim' ? '✅ Sim' : '❌ Não'}
• Formação Líderes: ${interesseFormacao === 'sim' ? '✅ Sim' : '❌ Não'}

📞 PRÓXIMOS PASSOS
Entre em contato para um plano personalizado de 90 dias
📱 WhatsApp: (48) 99157-5566
📧 E-mail: contato@temvenda.com.br`;

            const msg = encodeURIComponent(textoSimples);
            document.getElementById('whats_btn').href = "https://wa.me/5548991575566?text=" + msg;
            const assunto = encodeURIComponent("Diagnóstico TEM VENDA - " + lead.empresa);
            document.getElementById('mail_btn').href = "mailto:" + lead.email + "?subject=" + assunto + "&body=" + encodeURIComponent(textoSimples);

            window.scrollTo({top: document.getElementById('resultado').offsetTop, behavior: 'smooth'});
        }

        function copiarRelatorio() {
            // Usar o mesmo texto simples do WhatsApp
            const textoSimples = document.getElementById('report').textContent;
            navigator.clipboard.writeText(textoSimples).then(() => {
                alert('Relatório copiado para a área de transferência!');
            }).catch(() => {
                alert('Erro ao copiar. Tente selecionar o texto manualmente.');
            });
        }

        // Inicializar
        showStep(0);
    </script>
</body>
</html>
