import sys
import chess
import time
from evaluation import evaluate_board 

class MockfishEngine:
    def __init__(self):
        self.board = chess.Board()

    def search(self, time_limit=2.0):
        start_time = time.time()
        best_move = None
        max_depth = 1
        
        # Iterative Deepening
        while True:
            # Check time allocation
            if time.time() - start_time > time_limit:
                break
                
            # Search at fixed depth
            try:
                current_best = self.search_fixed_depth(max_depth)
                best_move = current_best
                
                # Info output (Standard UCI)
                print(f"info depth {max_depth} pv {best_move}")
                
                max_depth += 1
                if max_depth > 20: break # safety break
            except TimeoutError:
                break # stop if search runs too long inside recursion
                
        return best_move

    def search_fixed_depth(self, depth):
        best_move = None
        alpha = -float('inf')
        beta = float('inf')
        
        # Move Ordering: Captures first, then others
        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=lambda m: self.board.is_capture(m), reverse=True)

        if not legal_moves: return None
        
        best_val = -float('inf')

        for move in legal_moves:
            self.board.push(move)
            val = -self.alphabeta(depth - 1, -beta, -alpha)
            self.board.pop()
            
            if val > best_val:
                best_val = val
                best_move = move
            
            alpha = max(alpha, val)
        
        return best_move

    def alphabeta(self, depth, alpha, beta):
        
        if self.board.can_claim_draw():
            return 0

        if depth == 0 or self.board.is_game_over():
            return evaluate_board(self.board)
        
        legal_moves = list(self.board.legal_moves)
        if not legal_moves: 
            return evaluate_board(self.board) # Checkmate/Stalemate logic inside eval

        # Optimization: Sort captures first
        legal_moves.sort(key=lambda m: self.board.is_capture(m), reverse=True)

        for move in legal_moves:
            self.board.push(move)
            score = -self.alphabeta(depth - 1, -beta, -alpha)
            self.board.pop()
            
            if score >= beta: return beta # Cutoff
            if score > alpha: alpha = score
            
        return alpha

def main():
    engine = MockfishEngine()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line: break
            line = line.strip()
        except: break

        if line == "uci":
            print("id name Mockfish_HandCrafted")
            print("id author You")
            print("uciok")
        
        elif line == "isready":
            print("readyok")
            
        elif line.startswith("position"):
            parts = line.split()
            if "startpos" in parts:
                engine.board.reset()
            if "moves" in parts:
                idx = parts.index("moves")
                for move in parts[idx+1:]:
                    engine.board.push_uci(move)
                    
        elif line.startswith("go"):
            # Simple Time Management
            parts = line.split()
            wtime = 0
            btime = 0
            if "wtime" in parts: wtime = int(parts[parts.index("wtime")+1])
            if "btime" in parts: btime = int(parts[parts.index("btime")+1])
            
            my_time_ms = wtime if engine.board.turn == chess.WHITE else btime
            
            # Use 5% of time
            think_time = (my_time_ms / 1000) * 0.05 if my_time_ms > 0 else 1.0
            think_time = max(0.1, min(5.0, think_time)) # safety clamps
            
            move = engine.search(time_limit=think_time)
            
            if move:
                print(f"bestmove {move}")
            else:
                print("bestmove 0000") # resign
                
        elif line == "quit":
            break
        
        sys.stdout.flush()

if __name__ == "__main__":
    main()
