"""Seu analisador de defeitos (inclusão-exclusão), organizado em função reutilizável.

Convenção dos dados (em %), como no seu código original:
  apenas_A, apenas_B, apenas_C -> só aquele tipo de defeito
  A_e_B, A_e_C, B_e_C          -> exatamente aqueles dois (sem o terceiro)
  A_B_C                        -> os três ao mesmo tempo
"""

# Valores de exemplo, usados para gerar o dataset sintético
PERCENTUAIS_PADRAO = {
    "apenas_A": 1.0, "apenas_B": 3.0, "apenas_C": 6.0,
    "A_e_B": 1.0, "A_e_C": 1.5, "B_e_C": 2.0, "A_B_C": 0.5,
}


def calcular(d):
    """Recebe o dicionário de percentuais e devolve as probabilidades (em %)."""
    P_A = d["apenas_A"] + d["A_e_B"] + d["A_e_C"] + d["A_B_C"]
    P_B = d["apenas_B"] + d["A_e_B"] + d["B_e_C"] + d["A_B_C"]
    P_C = d["apenas_C"] + d["A_e_C"] + d["B_e_C"] + d["A_B_C"]
    P_AB = d["A_e_B"] + d["A_B_C"]
    P_AC = d["A_e_C"] + d["A_B_C"]
    P_BC = d["B_e_C"] + d["A_B_C"]
    P_ABC = d["A_B_C"]
    P_uniao = P_A + P_B + P_C - P_AB - P_AC - P_BC + P_ABC   # inclusão-exclusão
    return {
        "P_A": P_A, "P_B": P_B, "P_C": P_C,
        "P_AB": P_AB, "P_AC": P_AC, "P_BC": P_BC, "P_ABC": P_ABC,
        "P_uniao": P_uniao,
        "P_nenhum": 100 - P_uniao,
        "P_A_ou_B": P_A + P_B - P_AB,
        "soma_defeitos": sum(d.values()),
    }


def executar_interativo():
    print("=" * 70)
    print("ANALISADOR DE DEFEITOS EM APARELHOS DE TV")
    print("=" * 70)
    print("Digite os percentuais (ex.: '2' = 2%). Valores entre 0 e 100.\n")
    perguntas = [
        ("apenas_A", "Apenas defeitos críticos (A)"),
        ("apenas_B", "Apenas defeitos graves (B)"),
        ("apenas_C", "Apenas defeitos pequenos (C)"),
        ("A_e_B", "Críticos e graves (A∩B)"),
        ("A_e_C", "Críticos e pequenos (A∩C)"),
        ("B_e_C", "Graves e pequenos (B∩C)"),
        ("A_B_C", "Os três tipos (A∩B∩C)"),
    ]
    dados = {}
    try:
        for chave, texto in perguntas:
            v = float(input(f"  {texto}: "))
            if not 0 <= v <= 100:
                print(f"\n ERRO: {v}% fora do intervalo (0 a 100).")
                return None
            dados[chave] = v
    except ValueError:
        print("\n ERRO: digite apenas números válidos (ex: 2, 3.5, 10).")
        return None

    r = calcular(dados)
    if r["soma_defeitos"] > 100:
        print(f"\n ATENÇÃO: a soma dos defeitos é {r['soma_defeitos']:.1f}% (> 100%). Dados inconsistentes.")
        if input("Continuar mesmo assim? (s/n): ").lower() != "s":
            return None

    print("\n" + "=" * 70)
    print(" RESULTADOS")
    print("=" * 70)
    print(f"  P(A) = {r['P_A']:.1f}%   P(B) = {r['P_B']:.1f}%   P(C) = {r['P_C']:.1f}%")
    print(f"  a) Sem nenhum defeito:            {r['P_nenhum']:.1f}%")
    print(f"  b) Defeitos críticos OU graves:   {r['P_A_ou_B']:.1f}%")
    print("\n Passo a passo:")
    print(f"  P(A∪B∪C) = {r['P_A']:.1f} + {r['P_B']:.1f} + {r['P_C']:.1f} - {r['P_AB']:.1f} - "
          f"{r['P_AC']:.1f} - {r['P_BC']:.1f} + {r['P_ABC']:.1f} = {r['P_uniao']:.1f}%")
    print(f"  P(nenhum) = 100 - {r['P_uniao']:.1f} = {r['P_nenhum']:.1f}%")
    print(f"  P(A∪B) = {r['P_A']:.1f} + {r['P_B']:.1f} - {r['P_AB']:.1f} = {r['P_A_ou_B']:.1f}%")
    return r


if __name__ == "__main__":
    executar_interativo()
