from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from config import appConfig
from models.linkList import get_links_from_tags_lst, LinkList
from models.dbconf import dbConfig
import gui
import os


dbConfig.path = appConfig.db_path

Builder.load_string(appConfig.template)


#### MANAGER
class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        return ScreenManagement()


# def dir_exist_required(file=None):
#     def real_dec(f):
#         def decorator(*args, **kwargs):
#             data = kwargs['data']
#             path = file if file else data['name']
#             if os.path.exists(path):
#                 try:
#                     f(*args, **kwargs)
#                     return {"respond": True,
#                             "msg": "Success"}
#                 except:
#                     return {"respond": False,
#                             "msg": "Error"}
#             else:
#                 return {"respond": False,
#                         "msg": "Missing File"}

    #     return decorator
    # return real_dec

def db_file_exist(f):
    def decorator(*args, **kwargs):
        if os.path.exists(appConfig.db_path):
            print "Checking DB existence"
            f(*args, **kwargs)
            respond = {"respond": True,
                       "msg": "Success"}
        else:
            respond = {"respond": False,
                       "msg": "Missing Database File"}
        return respond
    return decorator


####
@db_file_exist
def search_btn_clicked(data=[], backref=None):

    query_res = get_links_from_tags_lst(data)
    print(query_res)

    backref(data=query_res)


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
           # print f.read()
            return f.read()

if __name__ == '__main__':
    gui.callbacks['search_btn_click'] = search_btn_clicked
    gui.callbacks['save_btn_click'] = save_btn_clicked
    gui.callbacks['on_lst_item_select'] = search_item_select
    gui.callbacks['get_instructions'] = instructions

    # gui.callbacks['file_selected'] = on_file_picked
    MyApp().run()
