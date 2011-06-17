from webpy.dark import *
from storm.locals import *
from model.customer import User
from model.users import *
from model.company import *
from model.client_prop import ClientProperty
from model.trans2 import *
from model.zoom import *

import sys
sys.stdout = sys.stderr


urls = (
    '', 'trans',
    'addtrans', 'addTrans',
    'request/(.*)', 'request',
    'propertysearch/', 'propertySearch',
    'get_trans_details', 'transactionDetails',
)

class trans:


    def GET(self):
        store = get_store()
        clients = store.find(Client)
        employees = store.find(Employee)
        return jrender('/transaction/transaction.html', {
            'clients':clients,
            'employees':employees
        })



class addTrans:
    '''
    Add a transaction
    '''


    def POST(self):
        i = web.input(survey={})
        store = get_store() 


        for k, v in i.items():
            if v == '' or v == None:
                del i[k]

        # PROPERTY CREATION
        if 'pid' not in i:
            prop = store.add(ClientProperty())
            prop.create(**i)
            
            store.flush()
            i['pid'] = prop.id
        
        # TRANSACTION CREATION
        t = store.add(Transaction())
        t.create(**i)        
        store.flush()
        i['trans_id'] = t.id

        # TRANSACTION CHILD
        if i['ttpe'] == 'New Lease':
            sub = store.add(NewLease())
        elif i['ttpe'] == 'Lease Extension':
            sub = store.add(LeaseExtension())
        elif i['ttpe'] == 'Purchase':
            sub = store.add(Purchase())
        elif i['ttpe'] == 'Sublease':
            sub = store.add(SubLease())
        elif i['ttpe'] == 'Lease Termination':
            sub = store.add(LeaseTermination())
        elif i['ttpe'] == 'Sale':
            sub = store.add(Sale())
        
        sub.create(**i)

        #SURVEY
        if i['survey'].filename != '':
            sent_date = i.get('survey_sent', '')
            zoom = Zoom(store, i['survey'])
            zoom.client_id = i['cid']
            if sent_date:
                zoom.sent_date = sent_date
            
            store.flush()
            t.survey_id = zoom.id

        store.commit()



class request:
    '''
    Return information for the ajax forms. 
    '''


    def POST(self, rtype):
        store = get_store()
        i = web.input()
        if rtype == 'companies':
            res = []
            client = store.find(Client, Client.id == int(i.id)).one()
            for comp in client.companies:
                res.append({'id':comp.id, 'title':comp.title})
            return return_json(res)

        elif rtype == 'divisions':
            res = []
            comp = store.find(Company, Company.id == int(i.id)).one()
            for div in comp.divisions:
                res.append({'id':div.id, 'title':div.title})
            return return_json(res)

        elif rtype== 'regions':
            res = []
            div = store.find(CompanyDivision, CompanyDivision.id == int(i.id)).one()
            for reg in div.regions:
                res.append({'id':reg.id, 'title':reg.title})
            return return_json(res)

        elif rtype == 'areas':
            res = []
            res.append({'id':1, 'title':'Fake Area'})
            return return_json(res)
    


class propertySearch:
    '''
    Used with the ajax auto complete
    '''


    def GET(self):
        i = web.input()
        store = get_store()
        results = store.find(ClientProperty, ClientProperty.address.like(unicode('%' + i.query + '%')))

        res = {
            'query':i.query,
            'suggestions':[],
            'data':[]
        }

        for prop in results:
            res['suggestions'].append(prop.address)
            res['data'].append(prop.id)

        return return_json(res)



class transactionDetails:
    '''
    Returns the proper fields depending on the type of transaction
    '''

    def POST(self):
        i = web.input()
        trans_type = i.get('type', None)
        type_dict = {
            'New Lease':'new_lease.html',
            'Lease Extension':'lease_ext.html',
            'Purchase':'purchase.html',
            'Sublease':'sublease.html',
            'Lease Termination':'lease_term.html',
            'Sale':'sale.html'
        }
        path = '/transaction/'

        return jrender(path + type_dict[trans_type])



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

