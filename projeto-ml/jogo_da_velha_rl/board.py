"""Funções do tabuleiro (adaptadas do seu código original).

O tabuleiro agora é uma lista simples de 9 posições (índices 0 a 8),
o que facilita transformar o estado em chave da Q-table.
Posição vazia = ' '.
"""

LINHAS_VENCEDORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # colunas
    (0, 4, 8), (2, 4, 6),              # diagonais
]


def novo_tabuleiro():
    return [' '] * 9


def display_board(board):
    """Mostra o tabuleiro no mesmo formato do seu código original."""
    print("+-------+-------+-------+")
    for r in range(3):
        c = [board[r * 3 + i] if board[r * 3 + i] != ' ' else str(r * 3 + i + 1)
             for i in range(3)]
        print("|       |       |       |")
        print(f"|   {c[0]}   |   {c[1]}   |   {c[2]}   |")
        print("|       |       |       |")
        print("+-------+-------+-------+")


def posicoes_livres(board):
    """Equivalente a make_list_of_free_fields (retorna índices 0-8)."""
    return [i for i, v in enumerate(board) if v == ' ']


def victory_for(board, sign):
    return any(board[a] == board[b] == board[c] == sign for a, b, c in LINHAS_VENCEDORAS)


def oponente(jogador):
    return 'O' if jogador == 'X' else 'X'
