def track_json_info(artist, album, title, art_url):
    import json
    return json.dumps({'artist':  artist,
                       'album':   album,
                       'title':   title,
                       'art_url': art_url})

def get_dbus_spotify():
    import dbus

    bus  = dbus.SessionBus()
    obj  = bus.get_object('org.mpris.MediaPlayer2.spotify', '/')
    spot = dbus.Interface(obj, 'org.freedesktop.MediaPlayer2')

    class DbusSpotify:
        def __init__(self, spot):
            self.iface = spot

        def play(self):
            self.iface.PlayPause()

        def next(self):
            self.iface.Next()

        def prev(self):
            self.iface.Previous()

        def current_track(self):
            info = self.iface.GetMetadata()
            return track_json_info(unicode(info['xesam:artist'][0]),
                                   unicode(info['xesam:album']),
                                   unicode(info['xesam:title']),
                                   unicode(info['mpris:artUrl']))

        def open_uri(self, uri):
            pass

    return DbusSpotify(spot)

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
            return track_json_info(track.artist(),
                                   track.album(),
                                   track.name(),
                                   uri)

        def open_uri(self, uri):
            pass

    return OsXSpotify(spot)

try:
    spotify = get_dbus_spotify()
except ImportError:
    spotify = get_osx_spotify()


# vim: filetype=python tabstop=4 shiftwidth=4 expandtab:
