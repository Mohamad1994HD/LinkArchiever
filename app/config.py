import os
import pkgutil

basedir = os.path.abspath(os.path.dirname(__file__))

# 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class Config:
    db_path = os.path.join(basedir, 'data-dev.sqlite')
    template = pkgutil.get_data('gui', 'app_gui.kv')
    instructions_path = os.path.join(basedir, 'instructions.txt')

class ProductionConfig(Config):
    db_path = os.path.join(basedir, 'data.sqlite ')


with open(os.path.join(basedir, "appConfig.json")) as jsonConf:
    import json
    jobj = json.loads(jsonConf.read())
    print jobj
    appConfig = ProductionConfig if jobj['state'] == 'production' else Config

