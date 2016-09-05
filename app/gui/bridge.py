
class Callbacks:
    on_search_btn_click = 'on_search_btn_click'
    on_save_btn_click = 'on_save_btn_click'
    on_lst_item_select = 'on_lst_item_select'
    on_file_not_found = 'on_file_not_found'
    get_instructions = 'get_instructions'
    on_result_data_ready = 'on_result_data_ready'


callbacks = {
    Callbacks.on_search_btn_click: None,
    Callbacks.on_save_btn_click: None,
    Callbacks.on_lst_item_select: None,
    Callbacks.on_file_not_found: None,
    Callbacks.get_instructions: None,
    Callbacks.on_result_data_ready: None
}