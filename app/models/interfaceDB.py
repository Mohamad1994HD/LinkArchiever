from sets import Set
from decorators import require_db_interaction

"""
This module contains basic functionality to interface the Database
1-def insert_link_with_tag(link, tag, new_link=False, new_tag=False, cursor=None):
2-def get_tag_id(tag_name, cursor=None):
3-def is_tag(tag_name):
4-def get_tag_data_from_id(id, cursor=None):
5-def get_links_ids_from_tags(tags, cursor=None):
6-def get_link_id(link_name, cursor=None):
7-def is_link(name):
8-def get_link_data_from_id(id, cursor=None):
"""





@require_db_interaction
def insert_link_with_tag(link, tag, existed_link=False, existed_tag=False, cursor=None):
    #
    try:
        if existed_tag and existed_link:
            return True

        if not existed_link:
            cursor.execute("""INSERT INTO links (link) VALUES (?) ;""", (link,))
        if not existed_tag:
            cursor.execute("""INSERT INTO tags (tag) VALUES (?);""", (tag,))

        cursor.execute("""INSERT INTO assc (links_id, tags_id) VALUES (
                            (SELECT id FROM links WHERE link=?),
                            (SELECT id FROM tags WHERE tag=?)
                        );""", (link, tag))
        return True
    except IOError as err:
        print ('Error: ' + str(err))
        return False


@require_db_interaction
def get_tag_id(tag_name, cursor=None):
    cursor.execute("""SELECT id FROM tags WHERE tag=?""", (tag_name, ))
    return cursor.fetchone()

@require_db_interaction
def get_tags_ids_of_link(link_name, cursor=None):
    cursor.execute("""SELECT id FROM tags WHERE id in (SELECT tags_id FROM assc WHERE links_id=(
    SELECT id FROM links WHERE link=?))""", (link_name,))
    return [k[0] for k in cursor.fetchall()]


# need change in query to accept array
@require_db_interaction
def get_tags_from_ids(ids, cursor=None):
    l = []
    for i in ids:
        cursor.execute("""SELECT tag FROM tags WHERE id=?;""", (i,))
        l.append(str(cursor.fetchone()[0]))
        # l.extend(k[0] for k in cursor.fetchall())
    return l


def is_tag(tag_name):
    return get_tag_id(tag_name=tag_name) is not None

@require_db_interaction
def get_tag_data_from_id(id, cursor=None):
    pass

# @require_db_interaction
# def get_links_ids_from_tags(tags, cursor=None):
#     cursor.execute("SELECT links.id FROM links")
#     tmp_set = Set([k[0] for k in cursor.fetchall()])
#     # print('before ' + str(tmp_set))
#     #
#     for tag in tags:
#         cursor.execute("""SELECT id FROM links WHERE id in
#         (SELECT links_id FROM assc WHERE tags_id = ( SELECT id FROM tags WHERE tag=?))""", (tag, )
#                        )
#         l = [k[0] for k in cursor.fetchall()]
#         if len(l) > 0:
#             tmp_set = tmp_set & Set(l)
#
#     return list(tmp_set)


@require_db_interaction
def get_links_ids_from_tag(tag_name, cursor=None):
    cursor.execute("""SELECT id FROM links WHERE id in
        (SELECT links_id FROM assc WHERE tags_id = ( SELECT id FROM tags WHERE tag LIKE ?))""",
                   ('%' + tag_name + '%', ))
    return [k[0] for k in cursor.fetchall()]


@require_db_interaction
def get_link_id(link_name, cursor=None):
    """
    :param link_name: string
    :param cursor: database cursor object
    :return: link id if exists
    """
    cursor.execute("""SELECT id FROM links WHERE link=?;""", (link_name,))
    return cursor.fetchone()[0] if cursor.fetchone() is not None else None


@require_db_interaction
def get_links_ids(cursor=None):
    cursor.execute("SELECT links.id FROM links")
    return [k[0] for k in cursor.fetchall()]


def is_link(name):
    """
         :param name: string
         :return: True if link existed, False otherwise
    """
    return get_link_id(link_name=name) is not None


@require_db_interaction
def get_link_name_desc_from_id(link_id, cursor=None):
    """
        :param link_id: integer
        :return: dictionary link_name,description, tags list
    """
    description = ''
    cursor.execute("""SELECT link,description FROM links WHERE id=?""", (link_id,))
    res = cursor.fetchone()
    name, desc = (str(res[0]), str(res[1]))

    return {'name': name, 'desc': desc}


def get_link_data_from_id(link_id):
    ans = get_link_name_desc_from_id(link_id=link_id)
    return {'name': ans['name'],
            'desc': ans['desc'],
            'tags': get_tags_from_ids(get_tags_ids_of_link(ans['name']))}