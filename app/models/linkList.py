from sets import Set

from interfaceDB import insert_link_with_tag, is_link, is_tag, get_tags_ids_of_link, get_tags_from_ids, \
    get_links_ids_from_tag, get_link_data_from_id


class LinkList(list):

    def __init__(self, link_name, link_desc=None, link_tags=[]):
        list.__init__([])
        self.name = link_name
        self.desc = link_desc
        self.extend(link_tags)

    def save_to_db(self):
        is_existed = is_link(self.name)
        for tag in self:
            insert_link_with_tag(self.name, tag, existed_link=is_existed, existed_tag=is_tag(tag_name=tag))

    def get_tags_from_db(self):
        del self[:]
        self.extend(get_tags_from_ids(get_tags_ids_of_link(self.name)))
        return self

    def __repr__(self):
        return str(self.repr())

    def repr(self):
        return {'name': self.name, 'desc': self.desc, 'tags': [i for i in self]}


def get_links_ids_from_tags_lst(tags):
    l = []
    for tag in tags:
        l.extend(get_links_ids_from_tag(tag))
    my_set = Set(l)
    return list(my_set)


def get_links_from_tags_lst(tags):
    ids = get_links_ids_from_tags_lst(tags)
    return [(get_link_data_from_id(id)) for id in ids]

