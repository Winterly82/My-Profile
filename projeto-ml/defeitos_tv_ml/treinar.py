"""Treina um Random Forest multirrótulo para prever defeitos A, B e C."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, multilabel_confusion_matrix,
                             precision_recall_curve, roc_auc_score)
from sklearn.model_selection import train_test_split

from .gerar_dados import CSV, gerar_dataset
from .probabilidades import PERCENTUAIS_PADRAO, calcular

PASTA = Path(__file__).parent
MODELO = PASTA / "modelo_defeitos.joblib"
ALVOS = ["defeito_A", "defeito_B", "defeito_C"]


def preparar_X(df):
    return pd.get_dummies(df.drop(columns=ALVOS, errors="ignore"), columns=["tipo_painel"])


def _probas(modelo, X):
    return np.column_stack([p[:, 1] for p in modelo.predict_proba(X)])


def _melhor_limiar(y_true, y_proba):
    """Limiar que maximiza o F1 (defeitos são raros, 0.5 quase nunca dispara)."""
    prec, rec, lim = precision_recall_curve(y_true, y_proba)
    f1 = 2 * prec[:-1] * rec[:-1] / np.clip(prec[:-1] + rec[:-1], 1e-9, None)
    return float(lim[np.argmax(f1)])


def treinar():
    df = pd.read_csv(CSV) if CSV.exists() else gerar_dataset()
    X, y = preparar_X(df), df[ALVOS]

    # treino / validação (escolhe limiares) / teste (nota final)
    X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    X_tr, X_val, y_tr, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, random_state=42)

    # Sem class_weight de propósito: assim as probabilidades ficam calibradas
    modelo = RandomForestClassifier(n_estimators=300, max_depth=8, min_samples_leaf=30,
                                    n_jobs=-1, random_state=42)
    modelo.fit(X_tr, y_tr)

    p_val, p_te = _probas(modelo, X_val), _probas(modelo, X_te)
    limiares = [_melhor_limiar(y_val.iloc[:, i], p_val[:, i]) for i in range(3)]
    pred = (p_te >= np.array(limiares)).astype(int)

    print("\n" + "=" * 70)
    print(" AVALIAÇÃO NO CONJUNTO DE TESTE")
    print("=" * 70)
    print(f" Limiares escolhidos na validação: " + ", ".join(
        f"{n[-1]}={t:.3f}" for n, t in zip(ALVOS, limiares)))
    print(classification_report(y_te, pred, target_names=ALVOS, zero_division=0))
    for i, nome in enumerate(ALVOS):
        print(f"  AUC {nome}: {roc_auc_score(y_te[nome], p_te[:, i]):.3f}")

    print("\n Matrizes de confusão [[VN FP] [FN VP]]:")
    for nome, m in zip(ALVOS, multilabel_confusion_matrix(y_te, pred)):
        print(f"  {nome}: {m.tolist()}")

    print("\n Importância das variáveis:")
    imp = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)
    for nome, v in imp.items():
        print(f"  {nome:<22} {v:.3f}")

    teoria = calcular(PERCENTUAIS_PADRAO)
    print("\n Teoria (inclusão-exclusão) x dados x modelo (média das probabilidades):")
    print(f"  {'':<8}{'Teoria':>9}{'Observado':>11}{'Modelo':>9}")
    for i, (nome, chave) in enumerate(zip(ALVOS, ["P_A", "P_B", "P_C"])):
        print(f"  {nome[-1]:<8}{teoria[chave]:>8.1f}%{y_te[nome].mean() * 100:>10.1f}%{p_te[:, i].mean() * 100:>8.1f}%")
    obs_ab = (y_te["defeito_A"] | y_te["defeito_B"]).mean() * 100
    mod_ab = (1 - (1 - p_te[:, 0]) * (1 - p_te[:, 1])).mean() * 100
    print(f"  {'A ou B':<8}{teoria['P_A_ou_B']:>8.1f}%{obs_ab:>10.1f}%{mod_ab:>8.1f}%  (modelo assume independência)")

    joblib.dump({"modelo": modelo, "colunas": list(X.columns), "limiares": limiares}, MODELO)
    print(f"\n Modelo salvo em {MODELO}")


if __name__ == "__main__":
    treinar()
