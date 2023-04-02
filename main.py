import datetime
import asyncio
import traceback

import discord
from discord.ext import tasks

import config
import librarymanager
import questionanswerer

print('init')

class Bot(discord.Client):

	libraryChannel = None
	versionsChannel = None
	accessRole = None

	async def on_ready(self):
		print(f'logged in as {self.user}')
		self.libraryChannel = await self.getChannelNamed('helper-bot-library')
		self.versionsChannel = await self.getChannelNamed('helper-bot-versions')
		self.activeServer = await self.fetch_guild(config.activeServerId)
		self.accessRole = self.activeServer.get_role(config.accessRoleId)

	async def on_message(self, curMessage):

		if curMessage.author == self.user:
			return

		if len(curMessage.content) == 0:
			return

		if curMessage.author.bot:
			return

		curMessageMember = await self.activeServer.fetch_member(curMessage.author.id)

		if curMessageMember == None:
			return

		if self.accessRole not in curMessageMember.roles:
			return

		if curMessage.channel == self.libraryChannel:
			async with curMessage.channel.typing():
				await librarymanager.newLibraryMessage(self, curMessage)
				return

		if curMessage.content.startswith('.q'):
			async with curMessage.channel.typing():
				await questionanswerer.questionTriggered(self, curMessage)
				return

	async def getChannelNamed(bot, givenName):
		for curChannel in bot.get_all_channels():
			if curChannel.name == givenName:
				return curChannel

if __name__ == '__main__':
	intents = discord.Intents.default()
	intents.presences = True
	intents.message_content = True
	intents.members = True
	bot = Bot(intents = intents)
	bot.run(config.discordBotToken)
