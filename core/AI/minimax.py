from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.chess_game.Board import ChessBoard
    from core.chess_game.player import Player
    from core.chess_game.Game import ChessGame
def minimax(game:'ChessGame', bot: 'Player' , depth:int, maximizing: bool, original_depth: int):

    if depth == 0 or game.Game_status():
        return Evaluate(bot)

    if maximizing:
        maxEval = - float('inf')
        best_move = None
        for piece in bot.get_pieces():
            piece_position = piece.get_position()  # piece return [r,c] = position, index = r * 8 + c
            from_index = piece_position[0] * 8 + piece_position[1]
            if not piece.is_captured():
                for to_position in piece.legal_move():
                    move = to_position[0] * 8 + to_position[1]
                    captured =  game.get_board().simulate_move(from_index, move)
                    eval_score = minimax(game, bot, depth - 1, False, original_depth)
                    game.get_board().undo_simulated_move(from_index, move, captured)
                    if eval_score > maxEval:
                        maxEval = eval_score
                        if depth == original_depth:  # chỉ lưu ở root
                            best_move = (from_index, move)
        if depth == original_depth:
            return best_move
        else:
            return maxEval  
    else:
        minEval = float('inf')
        best_move = None
        for piece in bot.get_opponent().get_pieces():
            piece_position = piece.get_position()  # piece return [r,c] = position, index = r * 8 + c
            from_index = piece_position[0] * 8 + piece_position[1]
            if not piece.is_captured():
                for to_position in piece.legal_move():
                    move = to_position[0] * 8 + to_position[1]
                    captured =  game.get_board().simulate_move(from_index, move)
                    eval_score =  minimax(game, bot, depth - 1, True, original_depth)
                    game.get_board().undo_simulated_move(from_index, move, captured)
                    if eval_score < minEval:
                        minEval = eval_score
                        if depth == original_depth:  # chỉ lưu ở root
                            best_move = (from_index, move)
        if depth == original_depth:
            return best_move
        else:
            return minEval                      

def Evaluate(player:'Player'):
    score = 0
    for piece in player.get_pieces():
        if not piece.is_captured():
            score += piece.get_value()
    
    for piece in player.get_opponent().get_pieces():
        if not piece.is_captured():
            score -= piece.get_value()
    return score