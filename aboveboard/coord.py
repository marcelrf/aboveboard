
class Coord:

    FILE_CODES = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self, file: int, rank: int):
        if file < 0 or file > 7:
            raise Exception(f"File coordinate {file} out of bounds.")
        if rank < 0 or rank > 7:
            raise Exception(f"Rank coordinate {rank} out of bounds.")
        self.file = file
        self.rank = rank

    @classmethod
    def from_notation(cls, notation: str):
        if len(notation) != 2:
            raise Exception(f"Invalid coord notation {notation}.")
        if notation[0] not in Coord.FILE_CODES:
            raise Exception(f"Invalid file notation {notation[0]}.")
        file = Coord.FILE_CODES.index(notation[0])
        try:
            rank = int(notation[1]) - 1
        except ValueError:
            raise Exception(f"Invalid rank notation {notation[1]}.")
        if rank < 0 or rank > 7:
            raise Exception(f"Invalid rank notation {notation[1]}.")
        return Coord(file, rank)
    
    def __eq__(self, other) -> bool:
        return self.file == other.file and self.rank == other.rank

    def to_string(self) -> str:
        return f"{Coord.FILE_CODES[self.file]}{self.rank + 1}"
