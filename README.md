# Aboveboard

A simple chess engine written just for fun.

## How to play
Python3 required. No need to install any libraries.
```
usage: play_aboveboard [-h] [-c {white,black,random}] [-l {0,1,2,3,4}]

Play a game of chess against the Aboveboard engine.

options:
  -h, --help            show this help message and exit
  -c {white,black,random}, --color {white,black,random}
                        The color of the pieces you want to play: white, black or random. Default: random.
  -l {0,1,2,3,4}, --level {0,1,2,3,4}
                        The level of difficulty: 0 (ridiculously easy) to 4 (medium). Default: 2.
```

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

## Potential improvements
- Add tests, comments, better documentation.
- Cache position evaluations, in case the same position needs to be evaluated in the future.
- Use bitboards to make operations/queries on boards more efficient (also would improve board hashes).
