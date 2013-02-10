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
            pass

        def open_uri(self, uri):
            pass

    return DbusSpotify(spot)

def get_osx_spotify():
    import ScriptingBridge

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
            pass

        def open_uri(self, uri):
            pass

    return OsXSpotify(spot)

try:
    spotify = get_dbus_spotify()
except ImportError:
    spotify = get_osx_spotify()
