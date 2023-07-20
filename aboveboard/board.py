
from aboveboard.coord import Coord
from aboveboard.piece import King, Queen, Rook, Bishop, Knight, Pawn, Piece, PieceColor
from typing import List


class Board:

    def __init__(self):
        self._board = [[None for file in range(8)] for rank in range(8)]
        self._white_pieces = []
        self._black_pieces = []
        self._piece_coords = {}
        self._populate_figures(PieceColor.BLACK, 7)
        self._populate_pawns(PieceColor.BLACK, 6)
        self._populate_pawns(PieceColor.WHITE, 1)
        self._populate_figures(PieceColor.WHITE, 0)

    def _populate_figures(self, color: PieceColor, rank: int) -> None:
        self.set_piece_at(Rook(color), Coord(0, rank))
        self.set_piece_at(Knight(color), Coord(1, rank))
        self.set_piece_at(Bishop(color), Coord(2, rank))
        self.set_piece_at(Queen(color), Coord(3, rank))
        self.set_piece_at(King(color), Coord(4, rank))
        self.set_piece_at(Bishop(color), Coord(5, rank))
        self.set_piece_at(Knight(color), Coord(6, rank))
        self.set_piece_at(Rook(color), Coord(7, rank))

    def _populate_pawns(self, color: PieceColor, rank: int) -> None:
        for i in range(8):
            self.set_piece_at(Pawn(color), Coord(i, rank))

    def get_pieces(self, color: PieceColor|None = None) -> List[Piece]:
        if color == PieceColor.WHITE:
            return self._white_pieces
        elif color == PieceColor.BLACK:
            return self._black_pieces
        else: # color is None
            return self._white_pieces + self._black_pieces
        
    def get_pawns(self, color: PieceColor|None = None) -> List[Pawn]:
        return [p for p in self.get_pieces(color) if type(p) == Pawn]
    
    def get_figures(self, color: PieceColor|None = None) -> List[Piece]:
        return [p for p in self.get_pieces(color) if type(p) != Pawn]

    def get_king(self, color: PieceColor) -> King|None:
        for piece in self.get_pieces(color):
            if type(piece) == King:
                return piece
        return None

    def get_piece_at(self, coord: Coord) -> Piece|None:
        return self._board[coord.file][coord.rank]

    def set_piece_at(self, piece: Piece, coord: Coord) -> None:
        self._board[coord.file][coord.rank] = piece
        self._piece_coords[piece] = coord
        if piece.color == PieceColor.WHITE:
            self._white_pieces.append(piece)
        else: # piece.color == PieceColor.BLACK
            self._black_pieces.append(piece)

    def remove_piece_at(self, coord: Coord) -> Piece:
        piece = self.get_piece_at(coord)
        self._board[coord.file][coord.rank] = None
        if piece not in self._piece_coords:
            print(coord.to_string())
        del self._piece_coords[piece]
        if piece.color == PieceColor.WHITE:
            self._white_pieces.remove(piece)
        else: # piece.color == PieceColor.BLACK
            self._black_pieces.remove(piece)
        return piece

    def get_piece_coord(self, piece: Piece) -> Coord:
        if piece not in self._piece_coords:
            raise Exception(f"Piece {piece.to_string()} not in board.")
        return self._piece_coords[piece]

    def to_string(self, reverse=False) -> str:
        text  = "    a   b   c   d   e   f   g   h    \n"
        text += "  .-------------------------------.  \n"
        for rank in range(7, -1, -1):
            piece_codes = []
            for file in range(8):
                piece = self.get_piece_at(Coord(file, rank))
                code = piece.to_string() if piece is not None else " "
                piece_codes.append(code)
            text += f"{rank + 1} | {' | '.join(piece_codes)} | {rank + 1}\n"
            if rank != 0:
                text += "  |-------------------------------|  \n"
        text += "  '-------------------------------'  \n"
        text += "    a   b   c   d   e   f   g   h    "
        if reverse:
            rows = text.split("\n")
            reversed_rows = [row[::-1] for row in reversed(rows)]
            text = "\n".join(reversed_rows)
        return text
