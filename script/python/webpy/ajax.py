import web

import json

def return_json(obj, status="200 OK"):
    """
    Return the obj as json
    """

    ret = json.dumps(obj)
    web.status = status
    web.header('Content-Type', 'application/json')
    web.header('Content-Length', len(ret))
    return ret

