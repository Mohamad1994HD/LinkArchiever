from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.listview import CompositeListItem, ListView
from kivy.adapters.dictadapter import DictAdapter
from kivy.utils import platform

callbacks = {
    'search_btn_click': None,
    'save_btn_click': None,
    'file_select_btn_click': None,
    'file_selected': None,
    'on_lst_item_select': None,
    'on_file_not_found_exception': None,
    'get_instructions':None
}


class MsgDialog(BoxLayout):
    msgtext = StringProperty()

    def __init__(self, msg=None, *args, **kwargs):
        super(MsgDialog, self).__init__(*args, **kwargs)
        self.popup = Popup(content=self,
                           size_hint=kwargs['size_hint'],
                           title=kwargs['title'])
        self.msgtext = msg

    def launch(self):
        self.popup.open()

    def close(self):
        self.popup.dismiss()


###### File picker #####
class FilePicker(BoxLayout):
    path = StringProperty("C://")
    path_text_view = ObjectProperty(None)

    def __init__(self, on_close, *args, **kwargs):
        super(FilePicker, self).__init__(*args, **kwargs)
        self.on_close = on_close
        self.path = kwargs['path']

    def file_selected(self, filename):
        callbacks['file_select_btn_click'](data=filename)

        self.on_close()
        pass




class CustomListItem(CompositeListItem):
    def __init__(self, *args, **kwargs):
        super(CustomListItem, self).__init__(*args, **kwargs)

    pass


######
class VPanel(BoxLayout):
    pass


class BaseWidget():
    pass


class NavigationBar():
    pass


#### HELP SCREEN ####
class InstructionsPanel(VPanel):
    inst_text = StringProperty()

    def __init__(self, *args, **kwargs):
        super(InstructionsPanel, self).__init__(*args, **kwargs)
        self.inst_text = self.get_inst_text()
        print self.inst_text

    def get_inst_text(self):
        return callbacks['get_instructions']()



class HelpScreenWidget:
    pass


class HelpScreen():
    pass


#### LICENSE SCREEN ####
class LicenseScreenWidget():
    pass


class LicenseScreen():
    pass


#### SAVE SCREEN ###
class SavePanel(VPanel):
    tags = ObjectProperty(None)
    fname = ObjectProperty(None)

    def btn_save_clk(self, data=''):
        # Reminder: put restrictions & exceptions
        # for faulty input like empty tags or path
        raw_data_tags = self.tags.text_input.text

        if len(raw_data_tags) < 3:
            msg = "Wrong input! please follow the Help section"
            MsgDialog(msg=msg, size_hint=(.8, .3), title='User Error').launch()

        else:
            tags_data = raw_data_tags.replace(" ", "").split(',')
            response = callbacks['save_btn_click'](data={'tags': tags_data,
                                                         'file': self.fname.filename_input.text}
                                                   )
            self.clear_inputs()

            msg = response["msg"]
            MsgDialog(msg=msg, size_hint=(.3, .3), title='Operation').launch()

    def clear_inputs(self):
        self.tags.text_input.text = ""
        self.fname.filename_input.text = ""


# class DriveSelection(DropDown):
#     pass

def get_win_drives():
    if platform == 'win':
        import win32api

        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]

        return drives
    else:
        return []

class FilePickerBar(BoxLayout):
    file_popup = ObjectProperty(None)
    filename_input = ObjectProperty(None)
    drop_down_btn = ObjectProperty(None)
    drive_selected = StringProperty('C://')

    def __init__(self, *args, **kwargs):
        super(FilePickerBar, self).__init__(*args, **kwargs)
        callbacks['file_select_btn_click'] = self.on_file_picked
        self.path = ''

    def drop_down_open(self):
        print "Drop Down open"
        from kivy.uix.button import Button
        drivers = get_win_drives()
        dropdown = DropDown()
        for driver in drivers:
            btn = Button(text=driver, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        dropdown.bind(on_select=self.select_root_path)
        dropdown.open(self.drop_down_btn)

    def select_root_path(self, instance, x):
        print x
        self.drive_selected = str(x).replace("\\", "//")

    def on_file_picked(self, data):
        self.filename_input.text = data
        # callbacks['file_selected'](data=data)

    def on_open_press(self):
        # initialize filepicker instance
        content = FilePicker(on_close=self.close_popup, path=self.drive_selected)

        self.file_popup = Popup(title='Select your file',
                                content=content,
                                size_hint=(.8, .8))
        self.file_popup.open()

    def close_popup(self):
        self.file_popup.dismiss()

    def commit_search_val(self):
        pass


class TagBar(BoxLayout):
    text_input = ObjectProperty(None)
    pass


class SaveScreenWidget():
    pass


class SaveScreen():
    pass


#### SEARCH SCREEN ####
class SearchBar(BoxLayout):
    search_txt = ObjectProperty(None)

    def btn_srch_clk(self):
        data = self.search_txt.text.replace(" ", "").split(',')
        # print data
        response = callbacks['search_btn_click'](data=data,
                                                 backref=callbacks['on_data_ready'])
        if not response["respond"]:
            msg = response["msg"]
            MsgDialog(msg=msg, size_hint=(.3, .3), title='Operation').launch()

    def commit_search_val(self):
        pass

    pass


class ResultBar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(ResultBar, self).__init__(*args, **kwargs)
        callbacks['on_data_ready'] = self.dump_data

    def dump_data(self, **kwargs):
        from lvargsconv import args_convertor
        items = {str(i): kwargs['data'][i] for i in range(len(kwargs['data']))}
        print items
        dict_adapter = DictAdapter(
            data=items,
            args_converter=args_convertor,
            selection_mode='single',
            allow_empty_selection=True,
            cls=CustomListItem)

        dict_adapter.bind(on_selection_change=self.on_select)

        self.clear_widgets()
        self.add_widget(ListView(adapter=dict_adapter))
        pass

    def on_select(self, dict_adapter):
        print dict_adapter.selection
        if len(dict_adapter.selection) > 0:
            dialog = MsgDialog(msg="Loading!", size_hint=(.3, .3), title='Operation')
            dialog.launch()
            response = callbacks['on_lst_item_select'](data=dict_adapter.data[str(dict_adapter.selection[0].index)])
            dialog.close()
            msg = response["msg"]
            MsgDialog(msg=msg, size_hint=(.3, .3), title='Operation').launch()
        pass

    pass


class SearchPanel():
    pass


class SearchScreen():
    pass
