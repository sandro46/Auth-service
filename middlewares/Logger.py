from flask import request

class Logger(object):
    def __init__(self, wapp, app):
        self.wapp = wapp
        self.app = app
    def __call__(self, environ, start_response):
        print ( '— — — — — — — — — — -')
        print ('Reques method is ')
        print (self.app.request.method)
        print ( '— — — — — — — — — — -')
        return self.app(environ, start_response)
