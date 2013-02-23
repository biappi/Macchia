import json

def get_dbus_spotify():
    import dbus
    import gobject
    import threading
    from dbus.mainloop.glib import threads_init, DBusGMainLoop

    gobject.threads_init()
    threads_init()

    class DbusSpotify:
        def __init__(self):
            loop = DBusGMainLoop(set_as_default=True)
            
            bus  = dbus.SessionBus()
            obj  = bus.get_object('org.mpris.MediaPlayer2.spotify', '/')

            self.iface = dbus.Interface(obj,
                                        'org.freedesktop.MediaPlayer2')
    
            service = bus.get_object('com.spotify.qt',
                                     '/org/mpris/MediaPlayer2')
        
            service.connect_to_signal('TrackChange',
                                      self.properties_changed)

            service.connect_to_signal('PropertiesChanged',
                                      self.properties_changed)
            
            self.notify_queue = None

        def properties_changed(self, *data):
            if self.notify_queue is not None:
                self.notify_queue.put_nowait('update')
    
        def play(self):
            self.iface.PlayPause()

        def next(self):
            self.iface.Next()

        def prev(self):
            self.iface.Previous()

        def current_track(self):
            info = self.iface.GetMetadata()
            artwork = info['mpris:artUrl'].replace('/thumb/', '/300/')

            artist = info.pop('xesam:artist')
            all_keys = [ unicode(x) for x in info.keys() ]

            full_info = {
                'xesam:artist': ', '.join([ unicode(x) for x in artist ]),
            }
            for x in all_keys:
                full_info[x] = unicode(info[x])

            url = info['xesam:url']
            url = url.replace('spotify:track:', 'http://open.spotify.com/track/')

            return json.dumps({
                'artist':    unicode(full_info['xesam:artist']),
                'album':     unicode(info['xesam:album']),
                'title':     unicode(info['xesam:title']),
                'art_url':   artwork,
                'trackid':   info['mpris:trackid'],
                'url':       url,
                'full_info': full_info,
            })
    
    return DbusSpotify()

def get_osx_spotify():
    import Foundation
    import ScriptingBridge
    import AppKit
    import base64

    spot = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.spotify.client")

    class OsXSpotify:
        def __init__(self, spot):
            self.iface = spot

        def play(self):
            self.iface.playpause()

        def next(self):
            self.iface.nextTrack()

        def prev(self):
            self.iface.previousTrack()

        def current_track(self):
            pool = Foundation.NSAutoreleasePool.alloc().init()
            track = self.iface.currentTrack()
            representation = track.artwork().representations()
            rep = AppKit.NSBitmapImageRep
            pngdata = rep.representationOfImageRepsInArray_usingType_properties_(representation,
                                                                                 AppKit.NSPNGFileType,
                                                                                 None)
            b64 = base64.b64encode(pngdata.bytes().tobytes())
            uri = 'data:image/png;base64,' + b64

            del pool
            return json.dumps({
                'artist':    track.artist(),
                'album':     track.album(),
                'title':     track.name(),
                'art_url':   uri,
                'trackid':   '',
                'url':       '',
                'full_info': {},
            })

        def open_uri(self, uri):
            pass

    return OsXSpotify(spot)

try:
    spotify = get_dbus_spotify()
except ImportError:
    spotify = get_osx_spotify()

# vim: filetype=python tabstop=4 shiftwidth=4 expandtab cindent:
