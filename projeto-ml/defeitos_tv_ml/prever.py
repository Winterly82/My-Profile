"""Prevê a probabilidade de defeitos de um novo aparelho."""
import joblib
import pandas as pd

from .treinar import ALVOS, MODELO, treinar


def prever(aparelho):
    if not MODELO.exists():
        print("Modelo ainda não treinado. Treinando agora...")
        treinar()
    pacote = joblib.load(MODELO)
    X = pd.get_dummies(pd.DataFrame([aparelho]), columns=["tipo_painel"])
    X = X.reindex(columns=pacote["colunas"], fill_value=0)
    probs = [float(p[0, 1]) for p in pacote["modelo"].predict_proba(X)]
    return dict(zip(ALVOS, probs))


def executar_interativo():
    print("=" * 70)
    print(" PREVISÃO DE DEFEITOS PARA UM NOVO APARELHO")
    print("=" * 70)
    try:
        aparelho = {
            "lote": int(input("  Lote (1 a 5): ")),
            "tipo_painel": input("  Painel (LED / QLED / OLED): ").strip().upper(),
            "horas_uso_dia": float(input("  Horas de uso por dia: ")),
            "idade_meses": int(input("  Idade do aparelho (meses): ")),
            "temperatura_media": float(input("  Temperatura média do ambiente (°C): ")),
        }
    except ValueError:
        print(" ERRO: entrada inválida.")
        return
    nomes = {"defeito_A": "críticos (A)", "defeito_B": "graves (B)", "defeito_C": "pequenos (C)"}
    print("\n Probabilidade estimada de defeitos:")
    r = prever(aparelho)
    for k, v in r.items():
        print(f"  {nomes[k]:<16} {v:6.1%}")
    sem = 1.0
    for v in r.values():
        sem *= (1 - v)
    print(f"  Algum defeito (aprox.): {1 - sem:6.1%}")
    print("\n Para comparar: a média geral da fábrica é A≈4%, B≈6,5%, C≈10%.")


if __name__ == "__main__":
    executar_interativo()
