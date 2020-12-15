from aiohttp import web
import aiohttp
import json

import sql

routes = web.RouteTableDef()

@routes.post('/')
async def handle(request):

    token = "^5oY7i$68qpC*&Z41hvTU5Q$b8MxfLUrJYRGM^hEoEb1y0CeOaPIprFqS2$F1B6uJ*1lybh%xEiboeh4QCoNqE!lGM0kcFaqQr^" # Same as Website API Token

    if not request.headers["token"]:
        return aiohttp.web.HTTPUnauthorized()

    if request.headers["token"] != token:
        return aiohttp.web.HTTPUnauthorized()

    if 'SessionGuilds' not in request.headers:
        return aiohttp.web.HTTPNotAcceptable()

    Guilds = {"Mutual": [], "NotMutual": []}

    servers = sql.GetGuilds()

    received = request.headers["SessionGuilds"].split()

    for i in received:
        if i in servers:
            Guilds["Mutual"].append(i)
        else:
            Guilds["NotMutual"].append(i)

    return web.json_response(Guilds)

@routes.post('/post')
async def handle(request):

    token = "^5oY7i$68qpC*&Z41hvTU5Q$b8MxfLUrJYRGM^hEoEb1y0CeOaPIprFqS2$F1B6uJ*1lybh%xEiboeh4QCoNqE!lGM0kcFaqQr^"
    if not request.headers["token"]:
        return aiohttp.web.HTTPUnauthorized()

    if request.headers["token"] != token:
        return aiohttp.web.HTTPUnauthorized()

    acceptedheaders = ['SimilarWords', 'Mentions', 'Capitals', 'Emojis', 'Invites', 'Joins', 'Swearing', 'Spam', 'Files', 'Spoilers']

    for i in acceptedheaders:
        if i in request.headers:
            if "Enabled" in request.headers:

                sql.Enable(request.headers[i], request.headers["Enabled"], acceptedheaders.index(i) + 1)

                return web.Response(text="Ok")

            if "Ignored" in request.headers:
                sql.Ignored(request.headers[i], request.headers["Ignored"], acceptedheaders.index(i) + 1)
                return web.Response(text="Ok")

            if "Ratelimit" in request.headers:
                sql.Ratelimit(request.headers[i], request.headers["Ratelimit"], acceptedheaders.index(i) + 1)
                return web.Response(text="Ok")

    if 'CoreSettings' in request.headers:

        if "Prefix" in request.headers:
            sql.SetSettings("Prefix", request.headers["CoreSettings"], request.headers["Prefix"])
            return web.Response(text="Ok")

        if "Channel" in request.headers:
            sql.SetSettings("Channel", request.headers["CoreSettings"], request.headers["Channel"])
            return web.Response(text="Ok")

        if "Language" in request.headers:
            sql.SetSettings("Language", request.headers["CoreSettings"], request.headers["Language"])
            return web.Response(text="Ok")

        if "IgnoredRoles" in request.headers:
            sql.SetSettings("IgnoredRoles", request.headers["CoreSettings"], request.headers["IgnoredRoles"])
            return web.Response(text="Ok")

        return web.Response(text="Ok")

    if 'AddRule' in request.headers:
        sql.AddRule(request.headers['AddRule'], request.headers['Type'], request.headers["Infractions"],
                    request.headers["Length"], request.headers["Increment"])

        return web.Response(text="Ok")

    if 'DeleteRule' in request.headers:
        sql.DeleteRule(request.headers["DeleteRule"], request.headers["Rule"])

        return web.Response(text="Ok")

    return aiohttp.web.HTTPUnauthorized()

@routes.post('/get')
async def handle(request):

    token = "^5oY7i$68qpC*&Z41hvTU5Q$b8MxfLUrJYRGM^hEoEb1y0CeOaPIprFqS2$F1B6uJ*1lybh%xEiboeh4QCoNqE!lGM0kcFaqQr^"

    if not request.headers["token"]:
        return aiohttp.web.HTTPUnauthorized()

    if request.headers["token"] != token:
        return aiohttp.web.HTTPUnauthorized()

    if 'GetGuildSettings' in request.headers:

        settings = sql.GetSettings(request.headers['GetGuildSettings'])

        return web.json_response(settings)

    if 'GetAutoModSettings' in request.headers:

        automod = sql.GetAutoModSettings(request.headers['GetAutoModSettings'])

        return web.json_response(automod)

    if 'GetLoggingPage' in request.headers:

        logs = sql.GetLogs(request.headers['GetLoggingPage'])

        logs = json.dumps(logs, sort_keys=True, default=str)

        return web.json_response(logs)

    if 'GetRules' in request.headers:

        logs = sql.GetRules(request.headers['GetRules'])

        return web.json_response(logs)

    return aiohttp.web.HTTPNotAcceptable()

app = web.Application()
app.add_routes(routes)
web.run_app(app)
