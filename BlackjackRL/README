# Reinforcement Learning for Blackjack

A SARSA(λ) agent learns to play blackjack from scratch via temporal-difference learning, with no built-in strategy rules, and is benchmarked against a naive heuristic and the mathematically optimal basic strategy.

## Main Findings

Across 10,000-hand evaluation runs:

| Strategy | Win % | Loss % | Push % |
|---|---|---|---|
| Vanilla (hit ≤16 / stand ≥17) | 38.45% | 51.06% | 10.49% |
| **TD-learned agent (SARSA(λ))** | **40.11%** | **52.03%** | **7.86%** |
| Basic strategy (theoretical optimum) | 43.42% | 48.03% | 8.55% |

- The TD agent beat the naive heuristic by ~1.7 points in win rate, learning entirely through self-play.
- It came within ~3.3 points of the theoretical-optimum basic strategy, despite using only a simple linear value approximation.
- Large-scale simulations (1M hands) confirm blackjack's inherent house edge even under perfect play (~43% player wins vs. ~48% dealer wins).
- Monte Carlo bankroll simulations show expected earnings decline and variance grows the longer a player plays.

## Takeaway

A general-purpose TD learning method can recover near-expert decision policies in blackjack purely from repeated play, without any hard-coded game knowledge.

## Tech Stack

Python, NumPy, Matplotlib, Seaborn — Jupyter notebook.
