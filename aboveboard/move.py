
from abc import ABC, ABCMeta
from aboveboard.coord import Coord
from aboveboard.piece import Queen, Rook, Bishop, Knight
from enum import Enum
import re


class CastlingMode(Enum):
    SHORT = 1
    LONG = 2


class Move(ABC):

    def __init__(self):
        """
        Should be implemented by all subclasses.
        """
        raise Exception("__init__ not implemented.")

    @classmethod
    def from_notation(cls, notation: str):
        """
        All subclasses should implement a method with this same signature
        called _from_notation, so this method can call them.
        It should return a Move of the subclass type in question,
        that represents the move described by the notation string.
        Should expect long algebraic notation.
        """
        for subclass in [
            RegularMove, Capture, EnPassantCapture, Promotion, PromotionCapture, Castling
        ]:
            try:
                move = subclass._from_notation(notation)
            except Exception:
                continue
            return move
        raise Exception(f"Invalid notation {notation}.")
    
    def __eq__(self, other) -> bool:
        """
        Should be implemented by all subclasses.
        Should return True if self represents the same move as other.
        Should return False otherwise.
        """
        raise Exception("__eq__ not implemented.")

    def to_string(self) -> str:
        """
        Should be implemented by all subclasses.
        Should return a string with the notation of the move.
        Should use long algebraic notation.
        """
        raise Exception("to_string not implemented.")


class RegularMove(Move):

    NOTATION_REGEX = r"[abcdefgh][12345678]-[abcdefgh][12345678]"

    def __init__(
        self,
        origin: Coord,
        destination: Coord
    ):
        self.origin = origin
        self.destination = destination

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(RegularMove.NOTATION_REGEX, notation):
            raise Exception(f"Invalid regular move notation {notation}.")
        origin_notation, destination_notation = notation.split("-")
        origin = Coord.from_notation(origin_notation)
        destination = Coord.from_notation(destination_notation)
        return RegularMove(origin, destination)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == RegularMove and
            self.origin == other.origin and
            self.destination == other.destination
        )

    def to_string(self) -> str:
        return f"{self.origin.to_string()}-{self.destination.to_string()}"


class Capture(RegularMove):

    NOTATION_REGEX = r"[abcdefgh][12345678]x[abcdefgh][12345678]"

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(Capture.NOTATION_REGEX, notation):
            raise Exception(f"Invalid capture notation {notation}.")
        origin_notation, destination_notation = notation.split("x")
        origin = Coord.from_notation(origin_notation)
        destination = Coord.from_notation(destination_notation)
        return Capture(origin, destination)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == Capture and
            self.origin == other.origin and
            self.destination == other.destination
        )
    
    def to_string(self) -> str:
        return f"{self.origin.to_string()}x{self.destination.to_string()}"


class EnPassantCapture(Capture):

    NOTATION_REGEX = r"[abcdefgh][12345678]x[abcdefgh][12345678] e.p."

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(EnPassantCapture.NOTATION_REGEX, notation):
            raise Exception(f"Invalid en passant capture notation {notation}.")
        notation = notation[0:-5] # remove e.p. suffix
        origin_notation, destination_notation = notation.split("x")
        origin = Coord.from_notation(origin_notation)
        destination = Coord.from_notation(destination_notation)
        return EnPassantCapture(origin, destination)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == EnPassantCapture and
            self.origin == other.origin and
            self.destination == other.destination
        )
    
    def to_string(self) -> str:
        return f"{self.origin.to_string()}x{self.destination.to_string()} e.p."


class Promotion(RegularMove):

    NOTATION_REGEX = r"[abcdefgh][12345678]-[abcdefgh][12345678]=[QRBN]"

    PROMOTE_CODE_MAP = {
        "Q": Queen,
        "R": Rook,
        "B": Bishop,
        "N": Knight
    }

    def __init__(
        self,
        origin: Coord,
        destination: Coord,
        promote_to: ABCMeta
    ):
        super().__init__(origin, destination)
        self.promote_to = promote_to

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(Promotion.NOTATION_REGEX, notation):
            raise Exception(f"Invalid promotion notation {notation}.")
        notation, promote_code = notation.split("=")
        origin_notation, destination_notation = notation.split("-")
        origin = Coord.from_notation(origin_notation)
        destination = Coord.from_notation(destination_notation)
        promote_to = Promotion.PROMOTE_CODE_MAP[promote_code]
        return Promotion(origin, destination, promote_to)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == Promotion and
            self.origin == other.origin and
            self.destination == other.destination and
            self.promote_to == other.promote_to
        )
    
    def to_string(self) -> str:
        reverse_promote_code_map = {v: k for k, v in Promotion.PROMOTE_CODE_MAP.items()}
        promote_code = reverse_promote_code_map[self.promote_to]
        return f"{self.origin.to_string()}-{self.destination.to_string()}={promote_code}"


class PromotionCapture(Capture):

    NOTATION_REGEX = r"[abcdefgh][12345678]x[abcdefgh][12345678]=[QRBN]"

    def __init__(
        self,
        origin: Coord,
        destination: Coord,
        promote_to: ABCMeta
    ):
        super().__init__(origin, destination)
        self.promote_to = promote_to

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(PromotionCapture.NOTATION_REGEX, notation):
            raise Exception(f"Invalid promotion capture notation {notation}.")
        notation, promote_code = notation.split("=")
        origin_notation, destination_notation = notation.split("x")
        origin = Coord.from_notation(origin_notation)
        destination = Coord.from_notation(destination_notation)
        promote_to = Promotion.PROMOTE_CODE_MAP[promote_code]
        return PromotionCapture(origin, destination, promote_to)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == PromotionCapture and
            self.origin == other.origin and
            self.destination == other.destination and
            self.promote_to == other.promote_to
        )
    
    def to_string(self) -> str:
        reverse_promote_code_map = {v: k for k, v in Promotion.PROMOTE_CODE_MAP.items()}
        promote_code = reverse_promote_code_map[self.promote_to]
        return f"{self.origin.to_string()}x{self.destination.to_string()}={promote_code}"


class Castling(Move):

    NOTATION_REGEX = r"(O-O|O-O-O)"

    def __init__(
        self,
        mode: CastlingMode
    ):
        self.mode = mode

    @classmethod
    def _from_notation(cls, notation: str):
        if not re.fullmatch(Castling.NOTATION_REGEX, notation):
            raise Exception(f"Invalid castling notation {notation}.")
        mode = CastlingMode.SHORT if notation == "O-O" else CastlingMode.LONG
        return Castling(mode)
    
    def __eq__(self, other) -> bool:
        return (
            type(other) == Castling and
            self.mode == other.mode
        )
    
    def to_string(self) -> str:
        if self.mode == CastlingMode.SHORT:
            return "O-O"
        else: # self.mode == CastlingMode.LONG
            return "O-O-O"
