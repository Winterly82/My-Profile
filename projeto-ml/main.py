"""Menu principal do projeto de Machine Learning."""
from jogo_da_velha_rl.play import jogar
from jogo_da_velha_rl.train import treinar as treinar_ia
from defeitos_tv_ml.probabilidades import executar_interativo as analisar_defeitos
from defeitos_tv_ml.gerar_dados import gerar_dataset
from defeitos_tv_ml.treinar import treinar as treinar_defeitos
from defeitos_tv_ml.prever import executar_interativo as prever_defeitos

MENU = """
======================================================================
 PROJETO DE MACHINE LEARNING
======================================================================
 JOGO DA VELHA (Aprendizado por Reforço)
  1) Treinar a IA (Q-Learning)
  2) Jogar contra a IA
 DEFEITOS DE TV (Aprendizado Supervisionado)
  3) Analisar probabilidades (inclusão-exclusão)
  4) Gerar dataset e treinar o modelo
  5) Prever defeitos de um novo aparelho
  0) Sair
"""


def main():
    acoes = {
        "1": treinar_ia,
        "2": jogar,
        "3": analisar_defeitos,
        "4": lambda: (gerar_dataset(), treinar_defeitos()),
        "5": prever_defeitos,
    }
    while True:
        print(MENU)
        op = input("Escolha: ").strip()
        if op == "0":
            print("Até logo!")
            break
        if op in acoes:
            acoes[op]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
