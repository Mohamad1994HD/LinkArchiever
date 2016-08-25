from kivy.uix.listview import ListItemButton, ListItemLabel

def args_convertor(row_index, rec):
    return  {'size_hint_y': None,
            'height': 70,
            'cls_dicts': [{'cls': ListItemButton,
                            'kwargs': {'text': 'Open',
                                       'size_hint_x': .10
                                       }
                           },
                        {'cls': ListItemLabel,
                            'kwargs': {'text': rec['name'],                                       
                                       'is_representing_cls': True,
                                       'size_hint_x': .70,
                                       }
                         },
                          {'cls': ListItemLabel,
                           'kwargs': {'text': str(rec['tags']),
                                      'size_hint_x': .20,
                                      }
                           }
                          ]
             }
          
"""
args_converter = lambda row_index, rec: \
            {'size_hint_y': None,
            'height': 70,
            'cls_dicts': [{'cls': ListItemButton,
                            'kwargs': {'text': 'Open',
                                       'size_hint_x': .10
                                       }
                           },
                        {'cls': ListItemLabel,
                            'kwargs': {'text': rec['path'],                                       
                                       'is_representing_cls': True,
                                       'size_hint_x': .70,
                                       }
                         },
                          {'cls': ListItemLabel,
                           'kwargs': {'text': str(rec['tags']),
                                      'size_hint_x': .20,
                                      }
                           }
                          ]
             }
"""
