from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message
import re
import json

class Playa(Plugin):
	CHESS_POST_TYPE = 'custom_chess-game-post'

	def __init__(self, engine='stockfish', engine_time_limit=0.5):
		super().__init__()
		self.engine = engine
		self.engine_time_limit = engine_time_limit

	@listen_to('.?', needs_mention=True)
	async def play(self, message: Message):
		message_type = message.body['data']['post']['type']
		if message.body['data']['channel_type'] != 'P' or re.search('^system_', message_type) != None:
			return

		message_is_move = message_type == self.CHESS_POST_TYPE

		if message_is_move:
			state = json.loads(message.text)
		else:
			self.driver.create_post(
				message.channel_id
				, "Sorry, must've fallen asleep for a bit. Let me catch up."
			)

			delve = re.search(r'(?i)\bdelve\b', message.text)
			state = None
			params = {
				"per_page": 10
			}
			while True:
				channel = self.driver.posts.get_posts_for_channel(message.channel_id, params=params)
				for post_id in channel['order']:
					post = channel['posts'][post_id]
					if post['type'] == self.CHESS_POST_TYPE:
						state = json.loads(post['message'])
						break
				else:
					if delve and channel['prev_post_id'] not in ("", None):
						params['before'] = channel['order'][-1]
						continue
				break

			if state == None:
				reply = "I don't see a game."
				if not delve:
					reply += "  \nIf you want me to keep looking, type `@{} delve`.".format(self.driver.username)
				self.driver.create_post(message.channel_id, reply)
				return

		if state['gameStatus'] not in ('New Game', 'In Play'):
			self.driver.create_post(
				message.channel_id
				, 'Good game.'
			)
			return

		if (state['playerBlack']['id'] == self.driver.user_id) ^ state['blackToMove']:
			if not message_is_move:
				self.driver.create_post(
					message.channel_id
					, "Isn't it your turn?"
				)
			return

		import chess
		import chess.engine
		import chess.pgn

		if state['pgn'] == '':
			game = chess.pgn.Game()
			board = game.board()
			board.turn = chess.BLACK if state['blackToMove'] else chess.WHITE
		else:
			import io

			game = chess.pgn.read_game(io.StringIO(state['pgn']))
			board = game.board()
			for move in game.mainline_moves():
				board.push(move)
			if board.is_game_over():
				self.driver.create_post(
					message.channel_id
					, "Isn't the game over?"
				)
				return

		engine = chess.engine.SimpleEngine.popen_uci(self.engine)
		result = engine.play(board, chess.engine.Limit(time=self.engine_time_limit))
		engine.quit()
		game.end().add_main_variation(result.move)
		board.push(result.move)

		state['blackToMove'] = not state['blackToMove']
		state['gameStatus'] = 'Checkmate' if board.is_checkmate() else 'In Play'
		exporter = chess.pgn.StringExporter(columns=None, headers=False, variations=False, comments=False)
		state['pgn'] = game.accept(exporter).rstrip('* ')

		self.driver.posts.create_post({
			'channel_id': message.channel_id
			, 'message': json.dumps(state)
			, 'type': self.CHESS_POST_TYPE
			, 'props': {}
		})
		if board.is_game_over():
			self.driver.create_post(
				message.channel_id
				, 'Good game.'
			)
