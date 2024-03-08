import os
from mmpy_bot import Bot, Settings
from mm_chess import Playa

bot = Bot(
	settings = Settings(
		MATTERMOST_URL = os.environ.get('MATTERMOST_URL'),
		BOT_TOKEN = os.environ.get('BOT_TOKEN'),
		BOT_TEAM = os.environ.get('BOT_TEAM'),
		#DEBUG = True,
	),
	plugins = [Playa()], 
)
bot.run()
