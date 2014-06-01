import tap
import urllib2

def pp():
    urllib2.urlopen('http://kanae.local:8080/play')
    return False

def n():
    urllib2.urlopen('http://kanae.local:8080/next')
    return True

def p():
    urllib2.urlopen('http://kanae.local:8080/prev')
    return True

t = tap.Tap()
t.on('play_pause', pp)
t.on('next_track', n)
t.on('prev_track', p)
t.run()


