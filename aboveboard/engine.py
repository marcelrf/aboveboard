
from aboveboard.eval import *
from aboveboard.game import Game
from aboveboard.move import Move, Capture, PromotionCapture, EnPassantCapture, Castling
from aboveboard.piece import PieceColor
from random import shuffle
from typing import List

class Engine:

    def __init__(self, min_max_depth: int):
        self.min_max_depth = min_max_depth

    def get_best_move(self, game: Game, move_eval_callback=None) -> Move:
        legal_moves = self._sort_legal_moves(game)
        best_move, alpha, beta = None, -1.1, 1.1
        if game.turn == PieceColor.WHITE:
            for move in legal_moves:
                game.apply_move(move)
                score = self.evaluate_min_max(game, alpha, beta, self.min_max_depth)
                if move_eval_callback is not None:
                    move_eval_callback(len(legal_moves), move, score)
                if score > alpha:
                    alpha = score
                    best_move = move
                game.unapply_last_move()
        else: # game.turn == PieceColor.BLACK
            for move in legal_moves:
                game.apply_move(move)
                score = self.evaluate_min_max(game, alpha, beta, self.min_max_depth)
                if move_eval_callback is not None:
                    move_eval_callback(len(legal_moves), move, score)
                if score < beta:
                    beta = score
                    best_move = move
                game.unapply_last_move()
        return best_move

    def evaluate_min_max(self, game: Game, alpha: float, beta: float, depth: int) -> float:
        if game.is_finished() or depth == 0:
            return self.evaluate(game)
        legal_moves = self._sort_legal_moves(game)
        if game.turn == PieceColor.WHITE:
            for move in legal_moves:
                game.apply_move(move)
                alpha = max(alpha, self.evaluate_min_max(game, alpha, beta, depth - 1))
                game.unapply_last_move()
                if beta <= alpha:
                    break
            return alpha
        else: # game.turn == PieceColor.BLACK
            for move in legal_moves:
                game.apply_move(move)
                beta = min(beta, self.evaluate_min_max(game, alpha, beta, depth - 1))
                game.unapply_last_move()
                if beta <= alpha:
                    break
            return beta
        
    def _sort_legal_moves(self, game: Game) -> List[Move]:
        legal_moves = game.legal_moves()
        shuffle(legal_moves)
        scored_legal_moves = []
        for move in legal_moves:
            if type(move) in [Capture, PromotionCapture, EnPassantCapture]:
                score = 4
            elif self._is_threatening(game, move):
                score = 3
            elif self._is_forward(game, move):
                score = 2
            else:
                score = 1
            scored_legal_moves.append((move, score))
        sorted_legal_moves = sorted(scored_legal_moves, key=lambda x: -x[1])
        return [m for m, _ in sorted_legal_moves]
    
    def _is_threatening(self, game: Game, move: Move) -> bool:
        if type(move) == Castling:
            castling_coords = game.get_castling_coords(move.mode)
            piece = game.board.get_piece_at(castling_coords["rook_origin"])
            threat_coords = piece.get_destinations(castling_coords["rook_origin"])
        else:
            piece = game.board.get_piece_at(move.origin)
            if type(piece) == Pawn:
                threat_coords = piece.get_destinations(move.destination, capture=True)
            else:
                threat_coords = piece.get_destinations(move.destination)
        for threat_coord_path in threat_coords:
            for threat_coord in threat_coord_path:
                threatened_piece = game.board.get_piece_at(threat_coord)
                if threatened_piece is not None:
                    if threatened_piece.color == game.turn:
                        break
                    else:
                        return True                
        return False

    def _is_forward(self, game: Game, move: Move) -> bool:
        if type(move) == Castling:
            return False
        if game.turn == PieceColor.WHITE:
            return move.destination.rank > move.origin.rank
        else: # game.turn == PieceColor.BLACK
            return move.destination.rank < move.origin.rank

    def evaluate(self, game: Game) -> float:
        if game.is_finished():
            winner = game.winner()
            if winner == PieceColor.WHITE:
                return 1.0
            elif winner == PieceColor.BLACK:
                return -1.0
            else:
                return 0.0
        return sum([
            eval_material(game) * 0.85,
            eval_position(game) * 0.1,
            eval_center_control(game) * 0.05
        ])
