
from aboveboard.board import Board
from aboveboard.coord import Coord
from aboveboard.move import (
    Move, RegularMove, Capture, EnPassantCapture,
    Promotion, PromotionCapture, Castling, CastlingMode
)
from aboveboard.piece import King, Queen, Rook, Bishop, Knight, Pawn, Piece, PieceColor
from collections import defaultdict
from typing import Dict, List


class Game:

    def __init__(self):
        self.board = Board()
        self.turn = PieceColor.WHITE
        self.is_check = False
        self._move_history = []
        self._repeated_positions = defaultdict(int)
        self._repeated_positions[self.board.to_string()] += 1
        self._legal_moves = [self._get_legal_moves()]

    def _get_other_turn(self) -> PieceColor:
        if self.turn == PieceColor.WHITE:
            return PieceColor.BLACK
        else: # self.turn == PieceColor.BLACK
            return PieceColor.WHITE

    def _is_attacked(self, coord: Coord, color: PieceColor) -> bool:
        for piece_type in [King, Queen, Rook, Bishop, Knight]:
            attacking_piece = piece_type(color)
            destinations = attacking_piece.get_destinations(coord)
            for destination_path in destinations:
                for destination in destination_path:
                    destination_piece = self.board.get_piece_at(destination)
                    if destination_piece is None:
                        continue
                    elif (
                        destination_piece.color != color and
                        type(destination_piece) == piece_type
                    ):
                        return True
                    else:
                        break
        pawn_rank = coord.rank + 1 if color == PieceColor.WHITE else coord.rank - 1
        for pawn_file in [coord.file - 1, coord.file + 1]:
            try:
                pawn_coord = Coord(pawn_file, pawn_rank)
            except Exception:
                continue
            pawn = self.board.get_piece_at(pawn_coord)
            if (
                pawn is not None and
                pawn.color != color and
                type(pawn) == Pawn
            ):
                return True
        return False
    
    def _piece_has_moved(self, piece: Piece) -> bool:
        for _, moved_pieces, _, _ in self._move_history:
            if piece in moved_pieces:
                return True
        return False
    
    def _can_capture_en_passant(self, destination: Coord) -> bool:
        if len(self._move_history) == 0:
            return False
        if destination.rank != (5 if self.turn == PieceColor.WHITE else 2):
            return False
        last_move, moved_pieces, _, _ = self._move_history[-1]
        if type(last_move) == Castling:
            return False
        piece = moved_pieces[0]
        return (
            type(piece) == Pawn and
            last_move.origin.file == destination.file and
            last_move.origin.rank == (1 if piece.color == PieceColor.WHITE else 6) and
            last_move.destination.file == destination.file and
            last_move.destination.rank == (3 if piece.color == PieceColor.WHITE else 4)
        )

    def _can_castle(self, mode: CastlingMode) -> bool:
        castling_coords = self.get_castling_coords(mode)
        king = self.board.get_piece_at(castling_coords["king_origin"])
        if king is None or type(king) != King or self._piece_has_moved(king):
            return False
        rook = self.board.get_piece_at(castling_coords["rook_origin"])
        if rook is None or type(rook) != Rook or self._piece_has_moved(rook):
            return False
        if self._is_attacked(castling_coords["king_origin"], self.turn):
            return False
        for coord in [castling_coords["rook_destination"], castling_coords["king_destination"]]:
            if self.board.get_piece_at(coord) is not None or self._is_attacked(coord, self.turn):
                return False
        if mode == CastlingMode.LONG:
            piece = self.board.get_piece_at(castling_coords["rook_extra_path"])
            if piece is not None:
                return False
        return True
    
    def _is_insufficient_material(self) -> bool:
        for color in [PieceColor.WHITE, PieceColor.BLACK]:
            pawns = self.board.get_pawns()
            if len(pawns) > 0:
                return False
            figures = self.board.get_figures()
            queens = [p for p in figures if type(p) == Queen]
            rooks = [p for p in figures if type(p) == Rook]
            bishops = [p for p in figures if type(p) == Bishop]
            knights = [p for p in figures if type(p) == Knight]
            if len(queens) > 0 or len(rooks) > 0 or len(bishops + knights) > 1:
                return False
        return True

    def _get_legal_pawn_moves(self) -> List[Move]:
        last_rank = 7 if self.turn == PieceColor.WHITE else 0
        legal_moves = []
        for pawn in self.board.get_pawns(self.turn):
            origin = self.board.get_piece_coord(pawn)
            # Get legal non-capture moves
            destinations = pawn.get_destinations(origin, capture=False)
            for destination_path in destinations:
                for destination in destination_path:
                    destination_piece = self.board.get_piece_at(destination)
                    if destination_piece is None:
                        if destination.rank == last_rank:
                            # Promotion
                            for promote_to in [Queen, Rook, Bishop, Knight]:
                                move = Promotion(origin, destination, promote_to)
                                legal_moves.append(move)
                        else:
                            # RegularMove
                            move = RegularMove(origin, destination)
                            legal_moves.append(move)
                    else:
                        break
            # Get legal capture moves
            destinations = pawn.get_destinations(origin, capture=True)
            for destination_path in destinations:
                for destination in destination_path:
                    if self._can_capture_en_passant(destination):
                        # EnPassantCapture
                        move = EnPassantCapture(origin, destination)
                        legal_moves.append(move)
                    else:
                        captured_piece = self.board.get_piece_at(destination)
                        if captured_piece is None or captured_piece.color == pawn.color:
                            break
                        elif destination.rank == last_rank:
                            # PromotionCapture
                            for promote_to in [Queen, Rook, Bishop, Knight]:
                                move = PromotionCapture(origin, destination, promote_to)
                                legal_moves.append(move)
                        else:
                            # Capture
                            move = Capture(origin, destination)
                            legal_moves.append(move)
        return legal_moves

    def _get_legal_figure_moves(self) -> List[Move]:
        legal_moves = []
        for figure in self.board.get_figures(self.turn):
            origin = self.board.get_piece_coord(figure)
            destinations = figure.get_destinations(origin)
            for destination_path in destinations:
                for destination in destination_path:
                    captured_piece = self.board.get_piece_at(destination)
                    if captured_piece is None:
                        # RegularMove
                        move = RegularMove(origin, destination)
                        legal_moves.append(move)
                    elif captured_piece.color != self.turn:
                        # Capture
                        move = Capture(origin, destination)
                        legal_moves.append(move)
                        break
                    else:
                        break
        return legal_moves

    def _get_legal_moves(self) -> List[Move]:
        legal_move_candidates = []
        legal_move_candidates.extend(self._get_legal_pawn_moves())
        legal_move_candidates.extend(self._get_legal_figure_moves())
        # Discard moves that leave king in check
        king_piece = self.board.get_king(self.turn)
        legal_moves = []
        for move in legal_move_candidates:
            self.apply_move(move, skip_legal_moves=True)
            king_coord = self.board.get_piece_coord(king_piece)
            leaves_king_in_check = self._is_attacked(king_coord, king_piece.color)
            self.unapply_last_move(skip_legal_moves=True)
            if not leaves_king_in_check:
                legal_moves.append(move)
        # Add legal castling moves
        for mode in [CastlingMode.SHORT, CastlingMode.LONG]:
            if self._can_castle(mode):
                move = Castling(mode)
                legal_moves.append(move)
        return legal_moves
    
    def get_castling_coords(self, mode) -> Dict[str, Coord]:
        king_origin = Coord(4, 0 if self.turn == PieceColor.WHITE else 7)
        if mode == CastlingMode.SHORT:
            king_destination = Coord(6, king_origin.rank)
            rook_origin = Coord(7, king_origin.rank)
            rook_destination = Coord(5, king_origin.rank)
            rook_extra_path = None
        else: # mode == CastlingMode.LONG
            king_destination = Coord(2, king_origin.rank)
            rook_origin = Coord(0, king_origin.rank)
            rook_destination = Coord(3, king_origin.rank)
            rook_extra_path = Coord(1, king_origin.rank)
        return {
            "king_origin": king_origin,
            "king_destination": king_destination,
            "rook_origin": rook_origin,
            "rook_destination": rook_destination,
            "rook_extra_path": rook_extra_path
        }

    def legal_moves(self) -> List[Move]:
        return self._legal_moves[-1]

    def apply_move(self, move: Move, skip_legal_moves: bool = False) -> None:
        if not skip_legal_moves and self.is_finished():
            raise Exception("Can not apply moves after game is finished.")
        if not skip_legal_moves and move not in self.legal_moves():
            raise Exception(f"{move.to_string()} is not a legal move.")
        moved_pieces = []
        
        captured_piece = None
        if type(move) in [Capture, PromotionCapture]:
            captured_piece = self.board.remove_piece_at(move.destination)
        elif type(move) == EnPassantCapture:
            capture_from = Coord(move.destination.file, move.origin.rank)
            captured_piece = self.board.remove_piece_at(capture_from)

        promoted_piece = None
        if type(move) == Castling:
            coords = self.get_castling_coords(move.mode)
            king_piece = self.board.remove_piece_at(coords["king_origin"])
            self.board.set_piece_at(king_piece, coords["king_destination"])
            rook_piece = self.board.remove_piece_at(coords["rook_origin"])
            self.board.set_piece_at(rook_piece, coords["rook_destination"])
            moved_pieces.append(king_piece)
            moved_pieces.append(rook_piece)
        else: # type(move) != Castling
            piece = self.board.remove_piece_at(move.origin)
            moved_pieces.append(piece)
            if type(move) in [Promotion, PromotionCapture]:
                promoted_piece = piece
                promote_to_piece = move.promote_to(self.turn)
                self.board.set_piece_at(promote_to_piece, move.destination)
            else:
                self.board.set_piece_at(piece, move.destination)

        self._move_history.append([move, moved_pieces, captured_piece, promoted_piece])
        self.turn = self._get_other_turn()
        king_piece = self.board.get_king(self.turn)
        king_coord = self.board.get_piece_coord(king_piece)
        self.is_check = self._is_attacked(king_coord, king_piece.color)
        self._repeated_positions[self.board.to_string()] += 1
        if not skip_legal_moves:
            self._legal_moves.append(self._get_legal_moves())


    def unapply_last_move(self, skip_legal_moves: bool = False) -> Move:
        last_move, _, captured_piece, promoted_piece = self._move_history.pop(-1)
        board_hash = self.board.to_string()
        self._repeated_positions[board_hash] -= 1
        if self._repeated_positions[board_hash] == 0:
            del self._repeated_positions[board_hash]
        if not skip_legal_moves:
            self._legal_moves.pop(-1)
        self.turn = self._get_other_turn()

        if type(last_move) == Castling:
            coords = self.get_castling_coords(last_move.mode)
            king_piece = self.board.remove_piece_at(coords["king_destination"])
            self.board.set_piece_at(king_piece, coords["king_origin"])
            rook_piece = self.board.remove_piece_at(coords["rook_destination"])
            self.board.set_piece_at(rook_piece, coords["rook_origin"])
        else: # type(last_move) != Castling
            piece = self.board.remove_piece_at(last_move.destination)
            if type(last_move) in [Promotion, PromotionCapture]:
                self.board.set_piece_at(promoted_piece, last_move.origin)
            else:
                self.board.set_piece_at(piece, last_move.origin)

        if type(last_move) in [Capture, PromotionCapture]:
            self.board.set_piece_at(captured_piece, last_move.destination)
        elif type(last_move) == EnPassantCapture:
            captured_from = Coord(last_move.destination.file, last_move.origin.rank)
            self.board.set_piece_at(captured_piece, captured_from)

        king_piece = self.board.get_king(self.turn)
        king_coord = self.board.get_piece_coord(king_piece)
        self.is_check = self._is_attacked(king_coord, king_piece.color)

    def is_finished(self) -> bool:
        return (
            len(self.legal_moves()) == 0 or
            max(self._repeated_positions.values()) >= 3 or
            self._is_insufficient_material()
        )

    def winner(self) -> PieceColor|None:
        if not self.is_finished():
            raise Exception("Game is not finished.")
        if (
            max(self._repeated_positions.values()) >= 3 or
            self._is_insufficient_material()
        ):
            return None
        elif self.is_check:
            return self._get_other_turn()
        else:
            return None

    def to_string(self, reverse=False) -> str:
        text = self.board.to_string(reverse)
        if self.is_finished():
            if self.winner() == PieceColor.WHITE:
                text += "Result: 1-0\n"
            elif self.winner() == PieceColor.BLACK:
                text += "Result: 0-1\n"
            else:
                text += "Result: ½-½\n"
        else:
            text += ("White" if self.turn == PieceColor.WHITE else "Black") + " to play.\n"
        return text
