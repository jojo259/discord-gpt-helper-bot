import requests
import json

import config

async def makeRequest(reqStr, systemMessage = 'You are an assistant.'):

	reqMessages = [
		{'role': 'system', 'content': systemMessage},
		{'role': 'user', 'content': reqStr}
	]

	reqHeaders = {
		'Content-type': 'application/json',
		'Authorization': f'Bearer {config.openAiKey}',
	}

	reqBody = {
		'model': config.gptModel,
		'messages': reqMessages,
		'temperature': 0,
		'max_tokens': 1024,
	}

	print('doing openai api request')
	apiReq = requests.post('https://api.openai.com/v1/chat/completions', headers = reqHeaders, json = reqBody, timeout = 1024)
	print('openai api response received')

	try:
		reponseStr = apiReq.json()['choices'][0]['message']['content']
	except:
		print(apiReq.text)
		return

	return reponseStr
