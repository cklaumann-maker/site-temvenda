"use client";

import { useEffect, useMemo, useState } from "react";

type FinanceDay = {
  date: string;
  weekday: string;
  sales: number;
  cash_in_forecast_total: number;
  cash_in_actual_money: number;
  cash_in_actual_pix: number;
  cash_in_actual_card: number;
  cash_in_actual_convenio: number;
  future_in_confirmed: number;
  purchases_planned: number;
  old_debts_paid: number;
  expenses_planned: number;
  expenses_paid: number;
  balance_projected: number;
  balance_real: number;
};

const API_URL = process.env.NEXT_PUBLIC_FINANCE_API_URL || "http://localhost:8001";

export default function FinanceiroPage() {
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [monthCode, setMonthCode] = useState("12-25");
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState<FinanceDay[]>([]);
  const [tab, setTab] = useState<"dashboard" | "cash" | "management">("dashboard");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const [cashForm, setCashForm] = useState({
    money: "",
    pix: "",
    card: "",
    convenio: "",
  });

  const [managementForm, setManagementForm] = useState({
    purchases_planned: "",
    old_debts_paid: "",
    future_in_confirmed: "",
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = window.localStorage.getItem("tv_finance_token");
      if (stored) {
        setToken(stored);
      }
    }
  }, []);

  async function login(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) {
        alert("Senha inválida.");
        return;
      }
      const data = await res.json();
      setToken(data.access_token);
      if (typeof window !== "undefined") {
        window.localStorage.setItem("tv_finance_token", data.access_token);
      }
      await loadMonth(monthCode, data.access_token);
    } catch (err) {
      console.error(err);
      alert("Erro ao fazer login.");
    } finally {
      setLoading(false);
    }
  }

  async function loadMonth(code: string, currentToken?: string) {
    if (!token && !currentToken) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/months/current?monthCode=${code}`, {
        headers: {
          Authorization: `Bearer ${currentToken || token}`,
        },
      });
      if (!res.ok) {
        if (res.status === 401) {
          alert("Sessão expirada. Faça login novamente.");
          setToken(null);
          if (typeof window !== "undefined") {
            window.localStorage.removeItem("tv_finance_token");
          }
        } else {
          alert("Erro ao carregar mês.");
        }
        return;
      }
      const data = await res.json();
      setDays(data.days);
    } catch (err) {
      console.error(err);
      alert("Erro ao carregar mês.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRefresh() {
    if (!token) return;
    if (!confirm("Isso vai recarregar o mês a partir da planilha e apagar lançamentos manuais. Deseja continuar?")) {
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/admin/refresh?monthCode=${monthCode}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        alert("Erro ao atualizar mês.");
        return;
      }
      await loadMonth(monthCode);
    } catch (err) {
      console.error(err);
      alert("Erro ao atualizar mês.");
    } finally {
      setLoading(false);
    }
  }

  function formatCurrency(value: number) {
    return value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  }

  const currentDay = useMemo(
    () => days.find((d) => d.date === selectedDate) || null,
    [days, selectedDate]
  );

  async function submitCash(e: React.FormEvent) {
    e.preventDefault();
    if (!token || !selectedDate) return;
    setLoading(true);
    try {
      const body = {
        money: Number(cashForm.money || 0),
        pix: Number(cashForm.pix || 0),
        card: Number(cashForm.card || 0),
        convenio: Number(cashForm.convenio || 0),
      };
      const res = await fetch(`${API_URL}/api/days/${selectedDate}/cash-entry`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        alert("Erro ao salvar entrada de caixa.");
        return;
      }
      await loadMonth(monthCode);
      alert("Entrada do dia salva com sucesso.");
    } catch (err) {
      console.error(err);
      alert("Erro ao salvar entrada de caixa.");
    } finally {
      setLoading(false);
    }
  }

  async function submitManagement(e: React.FormEvent) {
    e.preventDefault();
    if (!token || !selectedDate) return;
    setLoading(true);
    try {
      const body = {
        purchases_planned: Number(managementForm.purchases_planned || 0),
        old_debts_paid: Number(managementForm.old_debts_paid || 0),
        future_in_confirmed: Number(managementForm.future_in_confirmed || 0),
      };
      const res = await fetch(`${API_URL}/api/days/${selectedDate}/management`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        alert("Erro ao salvar ajustes.");
        return;
      }
      await loadMonth(monthCode);
      alert("Ajustes salvos com sucesso.");
    } catch (err) {
      console.error(err);
      alert("Erro ao salvar ajustes.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="tv-container">
      <div className="tv-card">
        <h1 className="tv-title">Fluxo de Caixa TEM VENDA</h1>
        <p className="tv-subtitle">
          Painel financeiro com horizonte diário, integrando previsões da planilha e lançamentos reais.
        </p>

        {!token ? (
          <form onSubmit={login} style={{ maxWidth: 320 }}>
            <label className="tv-label">Senha de acesso</label>
            <input
              type="password"
              className="tv-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Digite a senha única"
            />
            <div style={{ marginTop: 16 }}>
              <button className="tv-button" type="submit" disabled={loading}>
                {loading ? "Entrando..." : "Entrar"}
              </button>
            </div>
          </form>
        ) : (
          <>
            <div
              style={{
                display: "flex",
                gap: 12,
                alignItems: "center",
                marginBottom: 20,
                flexWrap: "wrap",
              }}
            >
              <div>
                <label className="tv-label">Mês (MM-YY)</label>
                <input
                  className="tv-input"
                  style={{ width: 120 }}
                  value={monthCode}
                  onChange={(e) => setMonthCode(e.target.value)}
                />
              </div>
              <button
                className="tv-button secondary"
                type="button"
                onClick={() => loadMonth(monthCode)}
                disabled={loading}
              >
                {loading ? "Carregando..." : "Carregar mês"}
              </button>
              <button
                className="tv-button"
                type="button"
                onClick={handleRefresh}
                disabled={loading}
              >
                Atualizar da planilha
              </button>
            </div>

            <div className="tv-tabs">
              <button
                className={`tv-tab ${tab === "dashboard" ? "active" : ""}`}
                onClick={() => setTab("dashboard")}
              >
                Dashboard
              </button>
              <button
                className={`tv-tab ${tab === "cash" ? "active" : ""}`}
                onClick={() => setTab("cash")}
                disabled={!selectedDate}
              >
                Entrada do dia
              </button>
              <button
                className={`tv-tab ${tab === "management" ? "active" : ""}`}
                onClick={() => setTab("management")}
                disabled={!selectedDate}
              >
                Ajustes
              </button>
            </div>

            {tab === "dashboard" && (
              <div className="tv-grid-2">
                <div style={{ maxHeight: 480, overflow: "auto" }}>
                  <table className="tv-table">
                    <thead>
                      <tr>
                        <th>Dia</th>
                        <th>Semana</th>
                        <th>Venda</th>
                        <th>Entradas</th>
                        <th>Despesas prev.</th>
                        <th>Pagamentos</th>
                        <th>Compras</th>
                        <th>Dívidas</th>
                        <th>Futuras</th>
                        <th>Saldo proj.</th>
                        <th>Saldo real</th>
                      </tr>
                    </thead>
                    <tbody>
                      {days.map((d) => {
                        const saldoRealNegativo = d.balance_real < 0;
                        return (
                          <tr
                            key={d.date}
                            style={{
                              background:
                                selectedDate === d.date ? "#eff6ff" : "transparent",
                              cursor: "pointer",
                            }}
                            onClick={() => {
                              setSelectedDate(d.date);
                              setTab("cash");
                            }}
                          >
                            <td>{new Date(d.date).getDate()}</td>
                            <td>{d.weekday}</td>
                            <td>{formatCurrency(d.sales)}</td>
                            <td>
                              {formatCurrency(
                                d.cash_in_actual_money +
                                  d.cash_in_actual_pix +
                                  d.cash_in_actual_card +
                                  d.cash_in_actual_convenio || d.cash_in_forecast_total
                              )}
                            </td>
                            <td>{formatCurrency(d.expenses_planned)}</td>
                            <td>{formatCurrency(d.expenses_paid)}</td>
                            <td>{formatCurrency(d.purchases_planned)}</td>
                            <td>{formatCurrency(d.old_debts_paid)}</td>
                            <td>{formatCurrency(d.future_in_confirmed)}</td>
                            <td className={d.balance_projected < 0 ? "tv-negative" : ""}>
                              {formatCurrency(d.balance_projected)}
                            </td>
                            <td className={saldoRealNegativo ? "tv-negative" : ""}>
                              {formatCurrency(d.balance_real)}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                <div>
                  <h3 className="tv-section-title">Resumo do dia selecionado</h3>
                  <p className="tv-section-subtitle">
                    Clique em um dia no horizonte para ver os detalhes e lançar movimentos.
                  </p>
                  {currentDay ? (
                    <div style={{ fontSize: 13, lineHeight: 1.6 }}>
                      <div>
                        <strong>Data:</strong>{" "}
                        {new Date(currentDay.date).toLocaleDateString("pt-BR")} (
                        {currentDay.weekday})
                      </div>
                      <div>
                        <strong>Vendas:</strong>{" "}
                        {formatCurrency(currentDay.sales)}
                      </div>
                      <div>
                        <strong>Entradas previstas:</strong>{" "}
                        {formatCurrency(currentDay.cash_in_forecast_total)}
                      </div>
                      <div>
                        <strong>Entradas reais:</strong>{" "}
                        {formatCurrency(
                          currentDay.cash_in_actual_money +
                            currentDay.cash_in_actual_pix +
                            currentDay.cash_in_actual_card +
                            currentDay.cash_in_actual_convenio
                        )}
                      </div>
                      <div>
                        <strong>Despesas previstas:</strong>{" "}
                        {formatCurrency(currentDay.expenses_planned)}
                      </div>
                      <div>
                        <strong>Pagamentos (despesas pagas):</strong>{" "}
                        {formatCurrency(currentDay.expenses_paid)}
                      </div>
                      <div>
                        <strong>Saldo projetado:</strong>{" "}
                        <span
                          className={
                            currentDay.balance_projected < 0 ? "tv-negative" : ""
                          }
                        >
                          {formatCurrency(currentDay.balance_projected)}
                        </span>
                      </div>
                      <div>
                        <strong>Saldo real:</strong>{" "}
                        <span
                          className={
                            currentDay.balance_real < 0 ? "tv-negative" : ""
                          }
                        >
                          {formatCurrency(currentDay.balance_real)}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <p style={{ fontSize: 13, color: "#6b7280" }}>
                      Nenhum dia selecionado. Use a tabela ao lado.
                    </p>
                  )}
                </div>
              </div>
            )}

            {tab === "cash" && selectedDate && (
              <form onSubmit={submitCash} style={{ marginTop: 12, maxWidth: 420 }}>
                <h3 className="tv-section-title">Entrada do dia</h3>
                <p className="tv-section-subtitle">
                  Lançamento real substitui a previsão de entrada para este dia.
                </p>
                <div style={{ display: "grid", gap: 12 }}>
                  <div>
                    <label className="tv-label">Dinheiro (R$)</label>
                    <input
                      className="tv-input"
                      value={cashForm.money}
                      onChange={(e) =>
                        setCashForm((f) => ({ ...f, money: e.target.value }))
                      }
                    />
                  </div>
                  <div>
                    <label className="tv-label">PIX (R$)</label>
                    <input
                      className="tv-input"
                      value={cashForm.pix}
                      onChange={(e) =>
                        setCashForm((f) => ({ ...f, pix: e.target.value }))
                      }
                    />
                  </div>
                  <div>
                    <label className="tv-label">Cartão (R$)</label>
                    <input
                      className="tv-input"
                      value={cashForm.card}
                      onChange={(e) =>
                        setCashForm((f) => ({ ...f, card: e.target.value }))
                      }
                    />
                  </div>
                  <div>
                    <label className="tv-label">Convênio (R$)</label>
                    <input
                      className="tv-input"
                      value={cashForm.convenio}
                      onChange={(e) =>
                        setCashForm((f) => ({ ...f, convenio: e.target.value }))
                      }
                    />
                  </div>
                </div>
                <div style={{ marginTop: 16 }}>
                  <button className="tv-button" type="submit" disabled={loading}>
                    {loading ? "Salvando..." : "Salvar entrada do dia"}
                  </button>
                </div>
              </form>
            )}

            {tab === "management" && selectedDate && (
              <form
                onSubmit={submitManagement}
                style={{ marginTop: 12, maxWidth: 420 }}
              >
                <h3 className="tv-section-title">Ajustes de gestão</h3>
                <p className="tv-section-subtitle">
                  Compras do dia, dívidas antigas pagas e futuras entradas confirmadas.
                </p>
                <div style={{ display: "grid", gap: 12 }}>
                  <div>
                    <label className="tv-label">Compras do dia (R$)</label>
                    <input
                      className="tv-input"
                      value={managementForm.purchases_planned}
                      onChange={(e) =>
                        setManagementForm((f) => ({
                          ...f,
                          purchases_planned: e.target.value,
                        }))
                      }
                    />
                  </div>
                  <div>
                    <label className="tv-label">
                      Dívidas antigas pagas no dia (R$)
                    </label>
                    <input
                      className="tv-input"
                      value={managementForm.old_debts_paid}
                      onChange={(e) =>
                        setManagementForm((f) => ({
                          ...f,
                          old_debts_paid: e.target.value,
                        }))
                      }
                    />
                  </div>
                  <div>
                    <label className="tv-label">
                      Futuras entradas confirmadas para o dia (R$)
                    </label>
                    <input
                      className="tv-input"
                      value={managementForm.future_in_confirmed}
                      onChange={(e) =>
                        setManagementForm((f) => ({
                          ...f,
                          future_in_confirmed: e.target.value,
                        }))
                      }
                    />
                  </div>
                </div>
                <div style={{ marginTop: 16 }}>
                  <button className="tv-button" type="submit" disabled={loading}>
                    {loading ? "Salvando..." : "Salvar ajustes"}
                  </button>
                </div>
              </form>
            )}
          </>
        )}
      </div>
    </div>
  );
}


