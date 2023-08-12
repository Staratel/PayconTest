
import aiohttp
import asyncio
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

urls = ['https://paycon.su/api1.php', 'https://paycon.su/api2.php']


async def get_url_data(url, session):
	r = await session.request('GET', url=f'{url}')
	data = await r.json(content_type='text/html')
	return data


async def get_json_data():
	# Для появления спинера. Анимацию не смог сделать, были мысли о запуске второго потока или, но не вышло с Gtk
	while Gtk.events_pending():
		Gtk.main_iteration()
	async with aiohttp.ClientSession() as session:
		tasks = []
		for url in urls:
			tasks.append(get_url_data(url, session))
		data = await asyncio.gather(*tasks, return_exceptions=True)

	result = []
	for dict in data:
		for i in dict:
			result.append(f"{i['name']} {i['price']}")
	return result