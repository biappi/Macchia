from spotify import spotify
import web

urls = (
    '/play', 'Play',
    '/prev', 'Prev',
    '/next', 'Next',
    '/info', 'Info',
    '/',     'Index'
)

app  = web.application(urls, globals())

class Index:
    def GET(self):
        raise web.seeother('/static/index.html')

class Play:
    def GET(self):
        spotify.play()
        return 'ok'

class Prev:
    def GET(self):
        spotify.prev()
        return 'ok'

class Next:
    def GET(self):
        spotify.next()
        return 'ok'

class Info:
    def GET(self):
        return spotify.current_track()

if __name__ == '__main__':
    app.run()
