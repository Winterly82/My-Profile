"""Treino por self-play (o agente joga contra si mesmo) + avaliação contra jogador aleatório."""
import random
from pathlib import Path

from .agent import QAgent, codificar_estado
from .board import novo_tabuleiro, posicoes_livres, victory_for, oponente

PASTA = Path(__file__).parent
MODELO = PASTA / "modelo_qtable.pkl"
GRAFICO = PASTA / "curva_aprendizado.png"


def jogar_episodio(agente):
    """Uma partida de self-play, atualizando a Q-table."""
    board, jogador, ultimo = novo_tabuleiro(), 'X', {}
    while True:
        s = codificar_estado(board, jogador)
        if jogador in ultimo:   # recompensa 0 pelo lance anterior (jogo continua)
            ps, pa = ultimo[jogador]
            agente.atualizar(ps, pa, 0.0, s, posicoes_livres(board))
        a = agente.escolher(board, jogador)
        board[a] = jogador
        ultimo[jogador] = (s, a)

        if victory_for(board, jogador):
            agente.atualizar(s, a, 1.0, None, [])                       # vencedor
            if oponente(jogador) in ultimo:
                agente.atualizar(*ultimo[oponente(jogador)], -1.0, None, [])  # perdedor
            return
        if not posicoes_livres(board):                                  # empate
            for p in ultimo:
                agente.atualizar(*ultimo[p], 0.5, None, [])
            return
        jogador = oponente(jogador)


def avaliar(agente, partidas=500):
    """Agente (guloso) contra jogador aleatório, alternando quem começa."""
    v = e = d = 0
    for i in range(partidas):
        meu = 'X' if i % 2 == 0 else 'O'
        board, vez = novo_tabuleiro(), 'X'
        while True:
            if vez == meu:
                a = agente.escolher(board, vez, guloso=True)
            else:
                a = random.choice(posicoes_livres(board))
            board[a] = vez
            if victory_for(board, vez):
                v, d = (v + 1, d) if vez == meu else (v, d + 1)
                break
            if not posicoes_livres(board):
                e += 1
                break
            vez = oponente(vez)
    return v / partidas, e / partidas, d / partidas


def treinar(episodios=60000, avaliar_a_cada=5000, verbose=True):
    agente = QAgent()
    historico = []
    eps_ini, eps_fim = 1.0, 0.05
    for ep in range(1, episodios + 1):
        agente.epsilon = max(eps_fim, eps_ini - (eps_ini - eps_fim) * ep / (episodios * 0.8))
        jogar_episodio(agente)
        if ep % avaliar_a_cada == 0:
            vit, emp, der = avaliar(agente)
            historico.append((ep, vit, emp, der))
            if verbose:
                print(f"  Episódio {ep:>6} | vitórias {vit:5.1%} | empates {emp:5.1%} | derrotas {der:5.1%}")
    agente.epsilon = 0.0
    agente.salvar(MODELO)
    if verbose:
        print(f"\n Modelo salvo em: {MODELO}  ({len(agente.q)} pares estado-ação aprendidos)")
    _plotar(historico)
    return agente


def _plotar(historico):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    eps = [h[0] for h in historico]
    plt.figure(figsize=(8, 4.5))
    plt.plot(eps, [h[1] * 100 for h in historico], label="Vitórias", marker="o")
    plt.plot(eps, [h[2] * 100 for h in historico], label="Empates", marker="o")
    plt.plot(eps, [h[3] * 100 for h in historico], label="Derrotas", marker="o")
    plt.xlabel("Episódios de treino")
    plt.ylabel("% contra jogador aleatório")
    plt.title("Curva de aprendizado do agente Q-Learning")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICO, dpi=120)
    plt.close()
    print(f" Gráfico salvo em: {GRAFICO}")


if __name__ == "__main__":
    treinar()
