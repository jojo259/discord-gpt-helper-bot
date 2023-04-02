import json

import apirequester

async def newLibraryMessage(bot, curMessage):

	currentLibrary = await getCurrentLibrary(bot)
	await bot.versionsChannel.send(currentLibrary)

	if curMessage.content.startswith('.setlibrary'):
		await setCurrentLibrary(bot, curMessage.content[len('.setlibrary '):])
		await cleanLibraryChannel(bot)
		return

	print(f'new library message: {curMessage.content}')

	promptStr = json.dumps(
		{
			'currentLibrary': currentLibrary,
			'newInformation': curMessage.content.replace('"', "'"),
			'task': 'Use the new information ("newInformation") to update the Library ("currentLibrary"). If the Library has no information, then create the Library with the new information. Include all new information in the Library. You can update previously existing information with the new information. Do not make up any new information that was not provided to you. The Library is written ONLY in plain English. The Library is written as a single paragraph. Be very concise. The Library does not ever refer to itself, it is purely a paragraph of external information. Output the updated Library. Output in JSON format, like {"newLibrary": "infohere"}, with only one field "newLibrary", which contains the new Library.'
		}
	)

	apiResp = await apirequester.makeRequest(promptStr)

	newLibrary = json.loads(apiResp).get('newLibrary', 'jsonfail')

	await setCurrentLibrary(bot, newLibrary)
	await cleanLibraryChannel(bot)

async def setCurrentLibrary(bot, currentLibrary):
	async for curMessage in bot.libraryChannel.history(limit = 100):
		if curMessage.author == bot.user:
			if curMessage.content.startswith('INFO:'):
				await curMessage.edit(content = f'INFO:\n{currentLibrary}')

async def getCurrentLibrary(bot):
	libraryMessage = False
	async for curMessage in bot.libraryChannel.history(limit = 100):
		if curMessage.author == bot.user:
			if curMessage.content.startswith('INFO:'):
				libraryMessage = curMessage
	if not libraryMessage:
		libraryMessage = await bot.libraryChannel.send('INFO:')

	return libraryMessage.content[len('INFO:\n'):]

async def cleanLibraryChannel(bot):
	libraryMessage = False
	async for curMessage in bot.libraryChannel.history(limit = 100):
		if curMessage.author == bot.user:
			if curMessage.reference != None:
				await curMessage.delete()
		else:
			await curMessage.delete()
