# Projeto de Machine Learning: Jogo da Velha (RL) + Defeitos de TV (ML supervisionado)

Dois projetos num só repositório, cada um com uma técnica diferente:

| Projeto | Técnica | Biblioteca |
|---|---|---|
| Jogo da Velha | Aprendizado por Reforço (Q-Learning, self-play) | Python puro |
| Defeitos de TV | Classificação multirrótulo (Random Forest) | scikit-learn |

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

O menu permite treinar a IA, jogar contra ela, analisar probabilidades,
gerar o dataset, treinar o modelo de defeitos e prever um novo aparelho.
Cada módulo também roda sozinho, por exemplo: `python -m jogo_da_velha_rl.train`.

## 1) Jogo da Velha com Q-Learning

- `board.py`: suas funções (`display_board`, `victory_for`, casas livres), adaptadas para lista de 9 posições.
- `agent.py`: o agente e a Q-table. Atualização: `Q(s,a) += α · (r + γ · max Q(s',a') − Q(s,a))`.
- `train.py`: o agente joga 60 mil partidas contra si mesmo (self-play) com estratégia ε-greedy
  (ε cai de 1.0 para 0.05) e é avaliado a cada 5 mil partidas contra um jogador aleatório.
  Gera `curva_aprendizado.png`.
- `play.py`: você (O) joga contra a IA (X).

Detalhe importante: o estado é codificado do ponto de vista de quem joga
(1 = minha peça, -1 = do oponente), então uma única Q-table serve para X e O.
Recompensas: vitória +1, empate +0.5, derrota −1.

Resultado esperado: ~93% de vitórias, ~7% de empates e 0% de derrotas contra o jogador aleatório.

## 2) Defeitos de TV com Random Forest

- `probabilidades.py`: seu analisador (inclusão-exclusão) como função reutilizável.
- `gerar_dados.py`: dataset sintético de 20 mil TVs. As proporções de defeitos A, B e C seguem os
  percentuais de `PERCENTUAIS_PADRAO`, mas o risco varia com lote, temperatura, horas de uso,
  idade e tipo de painel.
- `treinar.py`: Random Forest multirrótulo, limiares escolhidos em um conjunto de validação,
  avaliação com precisão, recall, AUC e matrizes de confusão, e comparação
  **teoria × dados × modelo**.
- `prever.py`: probabilidade de defeitos A, B e C para um aparelho novo.

Observações:
- O dataset é **sintético**: o modelo só "descobre" as regras que nós mesmos colocamos nele.
  Com dados reais da sua fábrica, basta substituir `dados_tvs.csv` mantendo as mesmas colunas.
- Defeitos raros dão F1 baixo com qualquer limiar. Por isso o AUC e a calibração das probabilidades
  são as métricas mais informativas aqui.
- No `treinar.py` o `class_weight` foi deixado de fora de propósito: ele melhora o recall, mas
  distorce as probabilidades.

## Ideias para evoluir

- Trocar a Q-table por uma rede neural (DQN com PyTorch) ou treinar contra um oponente minimax.
- Testar Gradient Boosting (XGBoost/LightGBM) e comparar com o Random Forest.
- Calibrar as probabilidades com `CalibratedClassifierCV`.
- Criar uma interface gráfica (Tkinter/Streamlit) para jogar e prever defeitos.
