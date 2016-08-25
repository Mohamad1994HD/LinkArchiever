from dbconf import dbConfig as config
import sqlite3


def require_db_interaction(f):
    def decorator(*args, **kwargs):
        conn = sqlite3.connect(config.path)
        cursor = conn.cursor()

        def dec():
            try:
                kwargs['cursor'] = cursor
                return f(*args, **kwargs)
            except StandardError as e:
                return {"response": False,
                        "msg": str(e)}

        data = dec()
        conn.commit()
        conn.close()
        return data
    return decorator