# Python 3!

import random

def show(board):
	print('+---+')
	print('|%s|' % board[0:3])
	print('|%s|' % board[3:6])
	print('|%s|' % board[6:9])
	print('+---+')

def streaks(board):
	# Diagonals
	yield (board[0+0*3], board[1+1*3], board[2+2*3])
	yield (board[2+0*3], board[1+1*3], board[0+2*3])
	# Rows
	for i in range(3):
		yield (board[0+i*3], board[1+i*3], board[2+i*3])
	# Cols
	for i in range(3):
		yield (board[i+0*3], board[i+1*3], board[i+2*3])

def find_winner(board):
	for streak in streaks(board):
		if streak[0] == streak[1] == streak[2]:
			if streak[0] == 'x': return 'x'
			elif streak[0] == 'o': return 'o'
	return None

def finished(board):
	return not not (board.find(' ') == -1 or find_winner(board))

def other_player(player):
	return 'x' if player == 'o' else 'o'

def free_pos(board):
	for i in range(9):
		if board[i] == ' ': yield i

def moves(board, to_play):
	for pos in free_pos(board):
		yield put(board, to_play, pos)

def put(board, player, pos):
	return board[:pos] + player + board[pos+1:]

def score(board, player, to_play):
	winner = find_winner(board)
	if winner: return 1 if winner == player else 0

	scores = [
		score(new_board, player, other_player(to_play))
		for new_board in moves(board, to_play)
	]
	if len(scores) == 0: return 0.5 # Tie

	# Assume that player `to_play` will choose the best outcome (max) and
	# that the other player will choose the worst outcome for `to_play` (min).

	# Future improvement: Consider that the other player might make mistakes
	# and choose the path that leads to the best chance for winning without
	# introducing chances for losing.

	acc = max if player == to_play else min
	return acc(scores)

def best_move(board, player):
	print("CALCULATING", end="", flush=True)

	# Recursively consider all possibilities
	moves = [
		(pos, score(put(board, player, pos), player, other_player(player)))
		for pos in free_pos(board)
	]

	best_score = max(y for x, y in moves)
	good_moves = [x for x, y in moves if y == best_score]
	print("\r           \r", end="", flush=True)
	return random.choice(good_moves)


board = "   " + "   " + "   "
while not finished(board):
	show(board)
	move = int(input("X's move [0-8]: "))
	if board[move] != ' ': continue
	board = put(board, 'x', move)
	if finished(board): break;

	show(board)
	move = best_move(board, 'o')
	print("O's move [0-8]: %i" % move)
	board = put(board, 'o', move)

show(board)
if find_winner(board):
	print("%s wins" % find_winner(board))
else:
	print("Tie")
