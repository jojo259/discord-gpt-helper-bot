import os

import dotenv
dotenv.load_dotenv()

debugMode = False

if 'debugmode' in os.environ:
	debugMode = True
	print('running in DEBUG mode')
else:
	print('running in PRODUCTION mode')

discordBotToken = os.environ['discordbottoken']
openAiKey = os.environ['openaikey']
gptModel = os.environ['gptmodel']
activeServerId = int(os.environ['activeserverid'])
accessRoleId = int(os.environ['accessroleid'])
