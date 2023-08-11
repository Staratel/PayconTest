
import aiohttp
import asyncio
import json

# https://paycon.su/api1.php
# https://paycon.su/api2.php

urls = ['https://paycon.su/api1.php', 'https://paycon.su/api2.php']


async def get_url_data(url, session):
	r = await session.request('GET', url=f'{url}')
	data = await r.json(content_type='text/html')
	return data


async def main(urls):
	async with aiohttp.ClientSession() as session:
		tasks = []
		for url in urls:
			tasks.append(get_url_data(url, session))
		result = await asyncio.gather(*tasks, return_exceptions=True)
	return result


def get_json_data():
	data = asyncio.run(main(urls))
	result = []
	for item in data:
		result += item

	return result
