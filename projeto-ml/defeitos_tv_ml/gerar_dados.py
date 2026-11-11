"""Gera um dataset sintético de TVs cujos defeitos seguem (em média) as probabilidades
do seu analisador, mas com risco variando conforme as características do aparelho."""
from pathlib import Path

import numpy as np
import pandas as pd

from .probabilidades import PERCENTUAIS_PADRAO

CSV = Path(__file__).parent / "dados_tvs.csv"

REGIOES = ["apenas_A", "apenas_B", "apenas_C", "A_e_B", "A_e_C", "B_e_C", "A_B_C"]
# (tem_A, tem_B, tem_C) de cada região; a posição 0 é "nenhum defeito"
FLAGS = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                  (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)])


def gerar_dataset(n=20000, percentuais=None, seed=42, salvar=True):
    rng = np.random.default_rng(seed)
    p = percentuais or PERCENTUAIS_PADRAO
    base = np.array([p[k] for k in REGIOES]) / 100

    lote = rng.integers(1, 6, n)
    painel = rng.choice(["LED", "QLED", "OLED"], n, p=[0.5, 0.3, 0.2])
    horas_uso_dia = rng.uniform(1, 12, n).round(1)
    idade_meses = rng.integers(1, 61, n)
    temperatura = rng.normal(28, 6, n).round(1)

    # Risco: lote 4 é pior, calor, uso intenso, aparelho velho e OLED aumentam a chance
    z = (1.2 * (lote == 4) + 0.8 * (temperatura - 28) / 6 + 0.7 * (horas_uso_dia - 6.5) / 3.5
         + 0.6 * (idade_meses - 30) / 17 + 0.5 * (painel == "OLED"))
    mult = np.exp(z)
    mult = np.clip(mult / mult.mean(), 0.2, 4)      # média 1 => mantém as proporções globais

    probs = base[None, :] * mult[:, None]
    soma = probs.sum(axis=1)
    probs[soma > 0.95] *= (0.95 / soma[soma > 0.95])[:, None]
    p_nenhum = 1 - probs.sum(axis=1)

    cum = np.cumsum(np.column_stack([p_nenhum, probs]), axis=1)
    idx = np.minimum((rng.random(n)[:, None] > cum).sum(axis=1), 7)
    f = FLAGS[idx]

    df = pd.DataFrame({
        "lote": lote, "tipo_painel": painel, "horas_uso_dia": horas_uso_dia,
        "idade_meses": idade_meses, "temperatura_media": temperatura,
        "defeito_A": f[:, 0], "defeito_B": f[:, 1], "defeito_C": f[:, 2],
    })
    if salvar:
        df.to_csv(CSV, index=False)
        print(f" Dataset salvo em {CSV} ({n} aparelhos)")
    return df


if __name__ == "__main__":
    gerar_dataset()
