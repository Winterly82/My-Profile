"""Agente de Q-Learning para o jogo da velha."""
import pickle
import random
from collections import defaultdict
from pathlib import Path

from .board import posicoes_livres


def codificar_estado(board, jogador):
    """Estado do ponto de vista de quem vai jogar:
    1 = minha peça, -1 = peça do oponente, 0 = vazio.
    Assim a mesma Q-table serve para jogar de X e de O."""
    return tuple(0 if v == ' ' else (1 if v == jogador else -1) for v in board)


class QAgent:
    def __init__(self, alpha=0.3, gamma=0.95, epsilon=1.0):
        self.alpha = alpha        # taxa de aprendizado
        self.gamma = gamma        # importância do futuro
        self.epsilon = epsilon    # chance de explorar (jogada aleatória)
        self.q = defaultdict(float)

    def escolher(self, board, jogador, guloso=False):
        livres = posicoes_livres(board)
        if not guloso and random.random() < self.epsilon:
            return random.choice(livres)
        s = codificar_estado(board, jogador)
        valores = [self.q[(s, a)] for a in livres]
        melhor = max(valores)
        return random.choice([a for a, v in zip(livres, valores) if v == melhor])

    def atualizar(self, estado, acao, recompensa, prox_estado, prox_livres):
        """Q(s,a) <- Q(s,a) + alpha * (r + gamma * max Q(s',a') - Q(s,a))"""
        melhor_prox = max((self.q[(prox_estado, b)] for b in prox_livres), default=0.0)
        antigo = self.q[(estado, acao)]
        self.q[(estado, acao)] = antigo + self.alpha * (recompensa + self.gamma * melhor_prox - antigo)

    def salvar(self, caminho):
        with open(Path(caminho), "wb") as f:
            pickle.dump(dict(self.q), f)

    @classmethod
    def carregar(cls, caminho):
        agente = cls(epsilon=0.0)
        with open(Path(caminho), "rb") as f:
            agente.q = defaultdict(float, pickle.load(f))
        return agente
