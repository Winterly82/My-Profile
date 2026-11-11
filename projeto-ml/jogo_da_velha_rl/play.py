"""Jogue contra a IA no terminal. Você é 'O' e a IA é 'X'."""
from .agent import QAgent
from .board import display_board, novo_tabuleiro, posicoes_livres, victory_for
from .train import MODELO, treinar


def jogada_humana(board):
    while True:
        try:
            m = int(input("Digite sua jogada (1-9): "))
            if not 1 <= m <= 9:
                print("Entrada inválida. Digite um número entre 1 e 9.")
                continue
            if board[m - 1] != ' ':
                print("Essa casa já está ocupada. Escolha outra.")
                continue
            board[m - 1] = 'O'
            return
        except ValueError:
            print("Entrada inválida. Digite um número entre 1 e 9.")


def jogar():
    if not MODELO.exists():
        print("Modelo ainda não treinado. Treinando agora (leva alguns segundos)...")
        agente = treinar()
    else:
        agente = QAgent.carregar(MODELO)

    while True:
        board = novo_tabuleiro()
        vez = 'X' if input("Quem começa? (1 = IA, 2 = você): ").strip() != '2' else 'O'
        while True:
            if vez == 'X':
                board[agente.escolher(board, 'X', guloso=True)] = 'X'
            else:
                display_board(board)
                jogada_humana(board)
            if victory_for(board, vez):
                display_board(board)
                print("A IA venceu!" if vez == 'X' else "Você venceu!")
                break
            if not posicoes_livres(board):
                display_board(board)
                print("Empate!")
                break
            vez = 'O' if vez == 'X' else 'X'
        if input("\nJogar de novo? (s/n): ").strip().lower() != 's':
            break


if __name__ == "__main__":
    jogar()
