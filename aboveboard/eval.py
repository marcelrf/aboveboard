
from aboveboard.coord import Coord
from aboveboard.piece import King, Queen, Rook, Bishop, Knight, Pawn, PieceColor
from aboveboard.game import Game


MATERIAL_POINTS = {
    King: 0,
    Queen: 9,
    Rook: 5,
    Bishop: 3,
    Knight: 3,
    Pawn: 1
}
def eval_material(game: Game) -> float:
    white_points = sum([
        MATERIAL_POINTS[type(p)] for p in game.board.get_pieces(PieceColor.WHITE)
    ])
    black_points = sum([
        MATERIAL_POINTS[type(p)] for p in game.board.get_pieces(PieceColor.BLACK)
    ])
    if white_points + black_points == 0:
        return 0.0
    return (float(white_points) / (white_points + black_points)) * 2 - 1


KING_POSITION_POINTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 1, 2, 2, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0]
]
QUEEN_POSITION_POINTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
ROOK_POSITION_POINTS = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 3, 3, 2, 2, 2],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 2, 3, 3, 2, 0, 0]
]
BISHOP_POSITION_POINTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [0, 2, 1, 1, 1, 1, 2, 0],
    [2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 0, 1, 1, 0, 3, 1],
    [1, 0, 1, 0, 0, 1, 0, 1]
]
KNIGHT_POSITION_POINTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 1, 1, 2, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
PAWN_POSITION_POINTS = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
def eval_position(game: Game) -> float:
    white_points, black_points = 0, 0
    for file in range(8):
        for rank in range(8):
            piece = game.board.get_piece_at(Coord(file, rank))
            if piece is not None:
                if piece.color == PieceColor.WHITE:
                    rank = 7 - rank
                if type(piece) == King:
                    points = KING_POSITION_POINTS[rank][file]
                elif type(piece) == Queen:
                    points = QUEEN_POSITION_POINTS[rank][file]
                elif type(piece) == Rook:
                    points = ROOK_POSITION_POINTS[rank][file]
                elif type(piece) == Bishop:
                    points = BISHOP_POSITION_POINTS[rank][file]
                elif type(piece) == Knight:
                    points = KNIGHT_POSITION_POINTS[rank][file]
                else: # type(piece) == Pawn
                    points = PAWN_POSITION_POINTS[rank][file]
                if piece.color == PieceColor.WHITE:
                    white_points += points
                else: # piece.color == PieceColor.BLACK
                    black_points += points
    if white_points + black_points == 0:
        return 0.0
    return (float(white_points) / (white_points + black_points)) * 2 - 1


CENTER_CONTROL_POINTS = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
CENTER_CONTROL_FACTORS = {
    King: 1,
    Queen: 1,
    Rook: 2,
    Bishop: 3,
    Knight: 3,
    Pawn: 4
}
def eval_center_control(game: Game) -> float:
    white_points, black_points = 0, 0
    for piece in game.board.get_pieces():
        piece_factor = CENTER_CONTROL_FACTORS[type(piece)]
        origin = game.board.get_piece_coord(piece)
        if type(piece) == Pawn:
            destinations = piece.get_destinations(origin, capture=True)
        else:
            destinations = piece.get_destinations(origin)
        for destination_path in destinations:
            for destination in destination_path:
                destination_piece = game.board.get_piece_at(destination)
                destination_points = CENTER_CONTROL_POINTS[destination.rank][destination.file]
                if piece.color == PieceColor.WHITE:
                    white_points += destination_points * piece_factor
                else: # piece.color == PieceColor.BLACK
                    black_points += destination_points * piece_factor
                if destination_piece is not None:
                    break
    if white_points + black_points == 0:
        return 0.0
    return (float(white_points) / (white_points + black_points)) * 2 - 1
