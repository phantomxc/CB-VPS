from webpy.dark import *
from model.customer import User
from model.zoom import Zoom
import web
urls = (
    '', 'zoom',
    '/', 'zoom',
    'import', 'zoom_import',
)
class zoom:
    def GET(self):
        return jrender('zoomerang.html')

class zoom_import:
    def POST(self):
        i = web.input(survey={})
        store = get_store()
        zoom = Zoom(store, i['survey'])

app = web.application(urls, locals())

