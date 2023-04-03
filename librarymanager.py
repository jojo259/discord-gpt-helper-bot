import json

import apirequester

from discord import File
import io
import requests

async def newLibraryMessage(bot, curMessage):

	currentLibrary = await getCurrentLibrary(bot)
	if bool(currentLibrary):
		await bot.versionsChannel.send(file=File(fp=io.StringIO(currentLibrary), filename="history.txt"))

	if curMessage.content.startswith('.setlibrary'):
		await setCurrentLibrary(bot, curMessage.content[len('.setlibrary '):])
		return

	print(f'new library message: {curMessage.content}')

	promptStr = json.dumps(
		{
			'currentLibrary': currentLibrary,
			'newInformation': curMessage.content.replace('"', "'"),
			'task': 'Use the new information ("newInformation") to update the Library ("currentLibrary"). Include all new information in the Library. You can update previously existing information with the new information. Do not make up any new information that was not provided to you. The Library is written ONLY in plain English. The Library is written as a single paragraph. Be very concise. The Library does not ever refer to itself, it is purely a paragraph of external information. Output the updated Library. Output in JSON format, like {"newLibrary": "infohere"}, with only one field "newLibrary", which contains the new Library.'
		}
	)

	apiResp = await apirequester.makeRequest(promptStr)

	newLibrary = json.loads(apiResp).get('newLibrary', 'jsonfail')

	await setCurrentLibrary(bot, newLibrary)

async def setCurrentLibrary(bot, currentLibrary):
	await cleanLibraryChannel(bot)
	if bool(currentLibrary):
		await bot.libraryChannel.send(file=File(fp=io.StringIO(currentLibrary), filename="library.txt"))

async def getCurrentLibrary(bot):
	async for curMessage in bot.libraryChannel.history(limit = 100):
		if curMessage.author == bot.user:
			if bool(curMessage.attachments):
				req = requests.get(curMessage.attachments[0].url)
				return req.content.decode(req.encoding)

	await setCurrentLibrary(bot, "")
	return ""

async def cleanLibraryChannel(bot):
	async for curMessage in bot.libraryChannel.history(limit = 100):
		await curMessage.delete()
