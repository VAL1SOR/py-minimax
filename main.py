import math

def minimax(position, depth, alpha, beta, maximizingPlayer, getMoves, staticEval):
  if depth == 0 or len(getMoves(position)) == 0:
    return staticEval(position)
  
  if maximizingPlayer:
    maxEval = -math.inf
    for move in getMoves(position):
      eval = minimax(move, depth - 1, alpha, beta, False, getMoves, staticEval)
      maxEval = max(maxEval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return maxEval
  else:
    minEval = math.inf
    for move in getMoves(position):
      eval = minimax(move, depth - 1, alpha, beta, True, getMoves, staticEval)
      minEval = min(minEval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return minEval