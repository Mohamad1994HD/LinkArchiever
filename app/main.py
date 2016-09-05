from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from config import appConfig
from models.linkList import get_links_from_tags_lst, LinkList
from models.dbconf import dbConfig
import gui
import os
from gui import bridge

dbConfig.path = appConfig.db_path

Builder.load_string(appConfig.template)


#### MANAGER
class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    title = 'LinkArchiever 1.0'
    icon = 'icon1.ico'

    def build(self):
        return ScreenManagement()


def db_file_exist(f):
    def decorator(*args, **kwargs):
        print "Checking db file existance"
        if os.path.exists(appConfig.db_path):
            print "DB File existed"
            f(*args, **kwargs)
            respond = {"respond": True,
                       "msg": "Success"}
        else:
            respond = {"respond": False,
                       "msg": "Missing Database File"}
        return respond
    return decorator


####
def return_result_to_gui(f):
    def dec(*args, **kwargs):
        return bridge.callbacks[bridge.Callbacks.on_result_data_ready](data=f(*args, **kwargs))
    return dec


@db_file_exist
@return_result_to_gui
def search_btn_clicked(data=[]):
    query_res = get_links_from_tags_lst(data)
    # print(query_res)
    return query_res


@db_file_exist
def save_btn_clicked(data={}):
    return LinkList(link_name=data['file'], link_tags=data['tags']).save_to_db()

def on_file_picked(data=''):
    print "File path picked\n %s" % data


def search_item_select(data=None):
    print "item selected %s" % data
    if os.path.exists(data['name']):
        os.startfile(data['name'])
        response = {"respond":True, "msg":"Success"}
    else:
        response = {"respond":False, "msg":"File doesn't exist anymore"}
    return response


def instructions():
    with open(appConfig.instructions_path) as f:
        return f.read()

if __name__ == '__main__':

    bridge.callbacks[bridge.Callbacks.get_instructions] = instructions
    bridge.callbacks[bridge.Callbacks.on_search_btn_click] = search_btn_clicked
    bridge.callbacks[bridge.Callbacks.on_save_btn_click] = save_btn_clicked
    bridge.callbacks[bridge.Callbacks.on_lst_item_select] = search_item_select

    MyApp().run()
