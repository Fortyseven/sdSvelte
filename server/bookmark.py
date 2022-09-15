import base64
import datetime
import sqlite3
from urllib import request
from flask import request, make_response
import db

# db = None


def getBookmarks():

    sql = "SELECT * FROM bookmarks ORDER BY id DESC"

    db.conn.row_factory = sqlite3.Row

    cur = db.conn.cursor()
    cur.execute(sql)

    # merges keys/values
    rows = dict(result=[dict(r) for r in cur.fetchall()])

    for r in rows['result']:
        r['image'] = base64.b64encode(r['image']).decode()
        r['thumbnail'] = base64.b64encode(r['thumbnail']).decode()
        # r['init_image'] = base64.b64encode(r['init_image'])

    return rows


def deleteBookmark():
    print("DELETE BOOKMARK", request)
    data = request.get_json()
    print("DELETE", data['id'])
    sql = "DELETE FROM bookmarks WHERE id=?"

    cur = db.conn.cursor()
    cur.execute(sql, (int(data['id']),))
    db.conn.commit()
    return "ok"


def saveBookmark():
    # TODO Include small reference thumbnail
    try:
        data = request.get_json()
        sql = '''
            INSERT INTO bookmarks(
                created, seed, prompt, ddim_steps, width, height, scale, ddim_eta, sampler, strength, thumbnail, image, init_image
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''

        image = base64.standard_b64decode(data['image'])
        thumb = base64.standard_b64decode(data['thumbnail'])
        init_image = None
        if 'init_image' in data:
            init_image = base64.standard_b64decode(data['init_image'])

        parms = (
            datetime.datetime.now(),
            int(data['seed']),
            data['prompt'],
            str(data['ddim_steps']),
            str(data['width']),
            str(data['height']),
            str(data['scale']),
            str(data['ddim_eta']),
            data['sampler'],
            data.get('strength', None),
            memoryview(thumb),
            memoryview(image),
            init_image
        )
        cur = db.conn.cursor()
        cur.execute(sql, parms)
        db.conn.commit()
        return "ok"
    except Exception as e:
        print("EXCEPTION", e)
