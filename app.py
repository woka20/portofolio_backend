from flask import Flask , request
import json,logging, sys
from logging.handlers import RotatingFileHandler
from flask_restful import Resource, Api, reqparse
from blueprints import app, manager, jwt
import logging
from werkzeug.contrib.cache import SimpleCache

cache=SimpleCache()

api=Api(app, catch_all_404s=True)

if __name__=="__main__":
    try:
        if sys.argv[1]=='db':
            manager.run()
    except:
        logging.getLogger().setLevel('INFO')
        formatter=logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)s} %(levelname)s-%(message)s")
        log_handler=RotatingFileHandler("%s/%s" % (app.root_path, "../storage/log/app.log"),
        maxBytes=10000, backupCount=10)
        # log_handler.setLevel(logging.ROOT)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.run(debug=True, host="0.0.0.0", port=5000)
    



