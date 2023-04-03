import json

import apirequester
import librarymanager

async def questionTriggered(bot, curMessage):
	if len(curMessage.content.split()) == 1:
		messagesStr = ''
		async for conversationMessage in curMessage.channel.history(limit = 8):
			if conversationMessage.author != bot.user:
				messagesStr += f'\n{conversationMessage.author.name}: {conversationMessage.content}'
		await answerQuestion(bot, curMessage.channel, messagesStr = messagesStr)
	else:
		await answerQuestion(bot, curMessage.channel, questionStr = curMessage.content[3:])

async def answerQuestion(bot, inChannel, questionStr = None, messagesStr = None):

	promptStr = json.dumps(
		{
			'library': await librarymanager.getCurrentLibrary(bot),
			'question': questionStr,
			'messaegs': messagesStr,
			'task': 'Answer the given question ("question") or guess what the question is based on the messages ("messages") given using the information provided in the Library ("library"). Do not answer the question if it is not directly about the topics covered in the Library. If there is no information in the Library to answer the question, then make up a question about the price. Only respond in JSON format. The JSON should be like {"question": "thequestionhere", "answer": "theanswerhere"}, with only one these two fields "question" and "answer". Re-write the question, correcting any mistakes.'
		}
	)

	apiResp = await apirequester.makeRequest(promptStr, systemMessage = f'You are an AI bot called {bot.user.name}.\nDo what the user says.')

	try:
		apiJson = json.loads(apiResp)
	except json.JSONDecodeError as e:
		print(e)
		print(apiResp)
		return

	apiQuestion = apiJson.get('question', '[question]')
	apiAnswer = apiJson.get('answer', '[answer]')

	await inChannel.send(f'**{apiQuestion}**\n{apiAnswer}')
