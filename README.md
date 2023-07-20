# Aboveboard

Aboveboard is a simple chess engine written just for fun.

## Features
- Based on a minimax algorithm.
- Implements alpha beta pruning.
- Pre-sorts the legal moves at each step of the tree to boost pruning.
- 3 evaluation functions: material, position and center control.
- Implements rules like 3-fold repetition, insufficient material, capturing en passant, castling rules, etc.
- Playable via the command line.
- Configurable level of difficulty.

## Caveats
- It lacks many optimizations and is written in python, so it is (very) slow.
- It ignores opening or end-game theory.

## Possible optimizations
- Cache position evaluations, in case the same position needs to be evaluated in the future.
- Use bitboards to make operations/queries on boards more efficient (also would improve board hashes).
