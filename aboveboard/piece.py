
from abc import ABC
from aboveboard.coord import Coord
from enum import Enum
from typing import List


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


class Piece(ABC):

    def __init__(self, color: PieceColor):
        self.color = color

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        """
        Should be implemented by all subclasses.
        Should return all board destination coordinates that the piece
        could travel to with one move from the given origin coordinate.
        The destinations should be formatted as a List[List[Coord]].
        The inner lists should be used to group the destinations that
        form an uninterrupted path on the same file, rank or diagonal.
        They should be in order, the ones closer to the origin first.
        Destinations not in a path, should be in a list by themselves.
        """
        raise Exception("get_destinations not implemented.")
    
    def to_string(self) -> str:
        """
        Should be implemented by all subclasses.
        Should return a string with the character code of the piece.
        Lowercase for white pieces, uppercase for black pieces.
        """
        raise Exception("to_string not implemented.")


class King(Piece):

    DESTINATIONS_MAP = [
        (-1, 1),  (0, 1),  (1, 1),
        (-1, 0),           (1, 0),
        (-1, -1), (0, -1), (1, -1)
    ]

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        destinations = []
        for file_inc, rank_inc in King.DESTINATIONS_MAP:
            file = origin.file + file_inc
            rank = origin.rank + rank_inc
            if file >= 0 and file < 8 and rank >= 0 and rank < 8:
                destination = Coord(file, rank)
                destinations.append([destination])
        return destinations

    def to_string(self) -> str:
        return "♔" if self.color == PieceColor.WHITE else "♚"


class Queen(Piece):

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        rook_destinations = Rook(self.color).get_destinations(origin)
        bishop_destinations = Bishop(self.color).get_destinations(origin)
        return rook_destinations + bishop_destinations

    def to_string(self) -> str:
        return "♕" if self.color == PieceColor.WHITE else "♛"


class Rook(Piece):

    DESTINATIONS_MAP = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        destinations = []
        for file_inc, rank_inc in Rook.DESTINATIONS_MAP:
            destination_path = []
            steps = 1
            while True:
                file = origin.file + file_inc * steps
                rank = origin.rank + rank_inc * steps
                if file >= 0 and file < 8 and rank >= 0 and rank < 8:
                    destination = Coord(file, rank)
                    destination_path.append(destination)
                    steps += 1
                else:
                    break
            if len(destination_path) > 0:
                destinations.append(destination_path)
        return destinations

    def to_string(self) -> str:
        return "♖" if self.color == PieceColor.WHITE else "♜"
    

class Bishop(Piece):

    DESTINATIONS_MAP = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        destinations = []
        for file_inc, rank_inc in Bishop.DESTINATIONS_MAP:
            destination_path = []
            steps = 1
            while True:
                file = origin.file + file_inc * steps
                rank = origin.rank + rank_inc * steps
                if file >= 0 and file < 8 and rank >= 0 and rank < 8:
                    destination = Coord(file, rank)
                    destination_path.append(destination)
                    steps += 1
                else:
                    break
            if len(destination_path) > 0:
                destinations.append(destination_path)
        return destinations

    def to_string(self) -> str:
        return "♗" if self.color == PieceColor.WHITE else "♝"


class Knight(Piece):

    DESTINATIONS_MAP = [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]

    def get_destinations(self, origin: Coord) -> List[List[Coord]]:
        destinations = []
        for file_inc, rank_inc in Knight.DESTINATIONS_MAP:
            file = origin.file + file_inc
            rank = origin.rank + rank_inc
            if file >= 0 and file < 8 and rank >= 0 and rank < 8:
                destination = Coord(file, rank)
                destinations.append([destination])
        return destinations

    def to_string(self) -> str:
        return "♘" if self.color == PieceColor.WHITE else "♞"


class Pawn(Piece):

    def get_destinations(self, origin: Coord, capture: bool) -> List[List[Coord]]:
        if (
            self.color == PieceColor.WHITE and origin.rank == 7 or
            self.color == PieceColor.BLACK and origin.rank == 0
        ):
            return []
        destinations = []
        rank_inc = 1 if self.color == PieceColor.WHITE else -1
        if capture:
            if origin.file != 0:
                destinations.append([Coord(origin.file - 1, origin.rank + rank_inc)])
            if origin.file != 7:
                destinations.append([Coord(origin.file + 1, origin.rank + rank_inc)])
        else: # not capture
            destination_path = []
            destination_path.append(Coord(origin.file, origin.rank + rank_inc))
            if (
                self.color == PieceColor.WHITE and origin.rank == 1 or
                self.color == PieceColor.BLACK and origin.rank == 6
            ):
                    destination_path.append(Coord(origin.file, origin.rank + rank_inc * 2))
            destinations.append(destination_path)
        return destinations

    def to_string(self) -> str:
        return "♙" if self.color == PieceColor.WHITE else "♟︎"
