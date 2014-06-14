import tornado.ioloop
from tornado.web import *
from utilities import *

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

class FileHandler(RequestHandler):
    def get(self, filename):
        var_dict = feed_variables(filename + '.shi')    
        self.write(str(var_dict))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/data/(.*)", FileHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
