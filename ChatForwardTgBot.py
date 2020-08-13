from aiohttp import web
import aiohttp
import datetime
from setting import web_server_setting, Tg_setting

routes = web.RouteTableDef()


async def sendMessage(textData):
    data = {'chat_id': Tg_setting['groupId'], 'text': textData}
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post('https://api.telegram.org/bot' + Tg_setting['token'] + '/sendMessage', data=data):
            pass


@routes.get('/')
async def get_handler(request):
    return web.Response(text='Python Robot Server is running')


@routes.post('/' + web_server_setting['post'])
async def post_handler(request):
    data = await request.post()
    try:
        name = data['name']
    except Exception:
        return web.Response(text='No_Name')
    try:
        perm = data['perm']
    except Exception:
        return web.Response(text='No_Perm')
    try:
        text = data['text']
    except Exception:
        text = ''
    try:
        server = data['server']
    except Exception:
        server = ''
    print('[{}] [{}]: [{}] {}: {}'.format(
        datetime.datetime.now().strftime('%m-%d %H:%M:%S'),
        server,
        perm,
        name,
        text
    ))
    textData = '[{}] {}: {}'.format(
        server,
        name,
        text
    )
    await sendMessage(textData)
    return web.Response(text='OK')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=web_server_setting['host'], port=web_server_setting['port'])
