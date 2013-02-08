import dbus
import web

urls = (
    '/play', 'Play',
    '/prev', 'Prev',
    '/next', 'Next',
    '/', 'Index'
)

app  = web.application(urls, globals())
bus  = dbus.SessionBus()
obj  = bus.get_object('org.mpris.MediaPlayer2.spotify', '/')
spot = dbus.Interface(obj, 'org.freedesktop.MediaPlayer2')

class Index:
    def GET(self):
        raise web.seeother('/static/index.html')

class Play:
    def GET(self):
        spot.PlayPause()
        return 'ok'

class Prev:
    def GET(self):
        spot.Previous()
        return 'ok'

class Next:
    def GET(self):
        spot.Next()
        return 'ok'

if __name__ == '__main__':
    app.run()
