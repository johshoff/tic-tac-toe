#!/usr/bin/env python3

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
			if streak[0] != ' ': return streak[0]
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

def memoize(func):
	past_results = {}

	def new_func(*args):
		if args in past_results:
			return past_results[args]

		result = func(*args)
		past_results[args] = result

		return result

	return new_func

past_results = {}

def score(board, player, to_play):
	key = lowest_symmetric_board(board), player, to_play
	#key = board, player, to_play
	if key in past_results:
		return past_results[key]

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
	result = acc(scores)

	past_results[key] = result

	return result

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

def rotated(board):
	'''Mirror board vertically

	>>> board = 'xox xooxo'
	>>> board != rotated(board)
	True
	>>> board == rotated(rotated(rotated(rotated(board))))
	True
	'''
	# 012    630
	# 345 -> 741
	# 678    852
	return board[6] + board[3] + board[0] +\
	       board[7] + board[4] + board[1] +\
	       board[8] + board[5] + board[2]

def mirrored(board):
	'''Mirror board vertically

	>>> mirrored('xox xooxo')
	'oxo xoxox'
	>>> board = 'xox xooxo'
	>>> board == mirrored(mirrored(board))
	True
	'''
	# 012    678
	# 345 -> 345
	# 678    012
	return board[6:8+1] +\
	       board[3:5+1] +\
	       board[0:2+1]

def player_value(player):
	if player == ' ': return 0
	if player == 'x': return 1
	if player == 'o': return 2

def board_value(board):
	mul = 1
	value = 0
	for player in board:
		value += player_value(player) * mul
		mul *= 3
	return value

def all_rotations(board):
	'''Return all rotations of a board (may include duplicates)

	>>> sorted(all_rotations('x o      '))
	['      o x', '  x     o', 'o     x  ', 'x o      ']
	'''
	b = board
	for i in range(4):
		yield b
		b = rotated(b)

def symmetric_boards(board):
	boards = set()
	boards.update(all_rotations(board))
	boards.update(all_rotations(mirrored(board)))
	return boards

@memoize
def lowest_symmetric_board(board):
	'''Return the symmetric board with the lowest board_value

	>>> lowest_symmetric_board('  o     x')
	'o x      '
	'''
	return min((board_value(sym), sym) for sym in symmetric_boards(board))[1]

def test():
	import doctest
	import sys
	x = doctest.testmod()
	if x.failed > 0:
		sys.exit(1)

def ai_player(board, token):
	move = best_move(board, token)
	print("%s's move [0-8]: %i" % (token.capitalize(), move))
	return move

def human_player(board, token):
	while True:
		move = int(input("%s's move [0-8]: " % token.capitalize()))
		if board[move] == ' ':
			return move
		print('Illegal move')

def play(player_x, player_o, current_player='x'):
	board = "   " + "   " + "   "
	do_move = { 'x': player_x, 'o': player_o }

	while not finished(board):
		show(board)
		move = do_move[current_player](board, current_player)
		board = put(board, current_player, move)
		if finished(board): break;

		current_player = other_player(current_player)

	show(board)
	if find_winner(board):
		print("%s wins" % find_winner(board))
	else:
		print("Tie")

play(human_player, ai_player, 'x')

print('Memoized %d scores' % len(past_results))
