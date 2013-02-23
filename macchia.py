from spotify import spotify

import web
import time
import Queue

urls = (
    '/play', 'Play',
    '/prev', 'Prev',
    '/next', 'Next',
    '/info', 'Info',
    '/streaming_info', 'StreamingInfo',
    '/',     'Index'
)

notifier_queue = Queue.Queue()
spotify.notify_queue = notifier_queue

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

class StreamingInfo:
    def GET(self):
        web.header('Content-type', 'text/html')
        web.header('Transfer-Encoding', 'chunked')
        
        # Yielding nothing to fill the buffers
        # in browsers.
        yield ' ' * 1024 + '<br>'

        while True:
            notifier_queue.get()
            yield """
                <script type="text/javascript">
                    (function () {
                        var info = %s
                        update(info)
                    })()
                </script>
            """ % (spotify.current_track(), )

if __name__ == '__main__':
    import threading
    threading.Thread(target=app.run).start()

    try:
        import gobject
        gobject.MainLoop().run()
    except:
        pass

