import asyncio
import json
from channels.consumer import AsyncConsumer
from django.core import management
from .models import Url

class UrlConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
        urls = Url.objects.all()
        tasks = [self.request_site_info(url) for url in urls]
        await asyncio.gather(*tasks)

    async def request_site_info(self, url):
        if url.site_info == '':
            message = json.dumps({
                'urls_processing_text': url.name + ' отправлен на обработку'
            })
            await self.send({
                'type': 'websocket.send',
                'text': message
            })
            await asyncio.sleep(url.seconds + url.minutes * 60)
            result = management.call_command('site_info', url.name)
        else:
            result = url.site_info

        if result == '':
            urls_processing_text = url.name + ' не удалось получить информацию о сайте'
            site_info_text = url.name + '\n'
        else:
            if url.site_info == '':
                urls_processing_text = url.name + ' обработан'
                url.site_info = result
                url.save()
            else:
                urls_processing_text = url.name + ' данные загружены'
            site_info_text = url.name + '\n' + result

        message = json.dumps({
            'urls_processing_text': urls_processing_text,
            'site_info_text': site_info_text
        })
        await self.send({
            'type': 'websocket.send',
            'text': message
        })
