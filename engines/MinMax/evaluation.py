import chess

# Centipawns using PeSTO
MATERIAL = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}


# Piece-Square Tables (PST)
# Defined from White's perspective.
# For Black, we mirror the square index (square ^ 56).


# Pawn: Rewards advancing and controlling the center

PAWN_PST = [
    0,  0,  0,  0,  0,  0,  0,  0,   
    5,  5,  5,  5,  5,  5,  5,  5,   
    10, 10, 20, 30, 30, 20, 10, 10,  
    5,  5, 10, 25, 25, 10,  5,  5,   
    0,  0,  0, 20, 20,  0,  0,  0,   
    5, 10, 15, 30, 30, 15, 10,  5,   
    50, 50, 50, 50, 50, 50, 50, 50,  
    0,  0,  0,  0,  0,  0,  0,  0    
]


# Knight: Strong in center, dead on edges
KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]


# Bishop: Avoid corners, aim for long diagonals
BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]


# Rook: Good on 7th rank, center files
ROOK_PST = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]


# Queen: Keep slightly centralized
QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]


# King (Middlegame): Safety in castle
KING_PST = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]


# Map piece types to their tables
PST_MAP = {
    chess.PAWN: PAWN_PST,
    chess.KNIGHT: KNIGHT_PST,
    chess.BISHOP: BISHOP_PST,
    chess.ROOK: ROOK_PST,
    chess.QUEEN: QUEEN_PST,
    chess.KING: KING_PST
}


def evaluate_board(board):
    # Always return negative for current player
    if board.is_checkmate():
        return -99999
    
    # Draw logic
    if board.is_insufficient_material() or board.is_stalemate():
        return 0

    score = 0
    
    for square, piece in board.piece_map().items():
        material_val = MATERIAL[piece.piece_type]
        
        pst_table = PST_MAP[piece.piece_type]
        
        # Mirroring
        pst_idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
        position_val = pst_table[pst_idx]
        
        total_val = material_val + position_val
        
        if piece.color == chess.WHITE:
            score += total_val
        else:
            score -= total_val
            
    # Negamax score
    return score if board.turn == chess.WHITE else -score
