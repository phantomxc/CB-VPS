from webpy.dark import *
from storm.locals import *
from model.customer import User
from model.users import *
from model.company import *
from model.report import Report


urls = (
    '', 'dash',
    '/', 'dash',
    'companies', 'dashCompanies',
    'filters', 'dashFilters',
    'report', 'buildReport',
)

class dash:
    def GET(self):
        store = get_store()
        clients = store.find(Client)
        return jrender('/dashboard/dashboard.html', {'clients':clients})



class dashCompanies:


    def POST(self):
        i = web.input()
        store = get_store()
        clients = store.find(Client)

        client_id = i.get('client_id', None)
        if client_id:
            selected_client = store.find(Client, Client.id == client_id).one()
        else:
            selected_client = clients[0]
    
        return jrender('/dashboard/companies.html', {
            'clients':clients,
            'selected_client':selected_client
        })



class dashFilters:


    def POST(self):
        i = web.input()
        active_tab = i.get('left_active_tab', None)

        if active_tab == 'Acquisitions':
            return jrender('/filters/acq_filters.html')
        elif active_tab == 'Dispositions':
            return jrender('/filters/disp_filters.html')



class buildReport:
    
    
    def POST(self):
        i = web.input(comp_cbox=[], div_cbox=[], reg_cbox=[], area_cbox=[])

        report = Report(companies=i.comp_cbox, divisions=i.div_cbox, regions=i.reg_cbox, areas=i.area_cbox, trans_obj=i.trans_obj)
        report.buildReport()

        if i.trans_obj == 'acquisition':
            return jrender('/dashboard/acq_report.html', {'report':report})
        else:
            return jrender('/dashboard/disp_report.html', {'report':report})

        


def session_auth():
    '''
    This entire app requires the user to be logged in
    '''
    sess = wsession()
    	
    if 'logged' in sess:
        if sess.logged != True:
            raise web.seeother('../login')
    else:
        raise web.seeother('../login')

app = web.application(urls, locals())
app.add_processor(web.loadhook(session_auth))

