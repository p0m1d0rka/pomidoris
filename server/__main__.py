from .db import DataBase
from .server import PomidorisServer
HOST = '127.0.0.1'
PORT = 65432
db = DataBase()


srv = PomidorisServer(host=HOST, port=PORT, db=db)
srv.register()
srv.serve()
