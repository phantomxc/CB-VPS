from webpy.dark import *
from storm.locals import *
from model.customer import User
from model.users import *
from model.company import *
from model.report import Report

from model.filters import FieldTypes
from model.filegen import *

import datetime

import ho.pisa as pisa
import tempfile


urls = (
    '', 'dash',
    '/', 'dash',
    'companies', 'dashCompanies',
    'filters', 'dashFilters',
    'filter_types', 'returnFilterTypes',
    'report', 'buildReport',
    'default_report', 'defaultReport',
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



class returnFilterTypes:
    """
    Pass the filter types to the javascript
    """

    def GET(self):
        types = FieldTypes()
        return return_json(types.returnTypes())



class defaultReport:

    def POST(self):
        
        i = web.input(comp_cbox=[], div_cbox=[], reg_cbox=[], area_cbox=[])
        
        reports = []

        report = Report(client_id=i.client_id, trans_obj=i.trans_obj)
        report.buildReport()
        reports.append(report)

        if i.trans_obj == 'acquisition':
            return jrender('/dashboard/acq_report.html', {'reports':reports})
        else:
            return jrender('/dashboard/disp_report.html', {'reports':reports})


class buildReport:
    
    
    def POST(self):
        i = web.input(comp_cbox=[], div_cbox=[], reg_cbox=[], area_cbox=[])
        
        reports = []
        
        # COMBINED REPORT
        if i.display == 'Combined':
            report = Report(client_id=i.client_id, companies=i.comp_cbox, divisions=i.div_cbox, regions=i.reg_cbox, areas=i.area_cbox, trans_obj=i.trans_obj, fiscal=i.fiscal)
            report.buildReport()
            reports.append(report)

        # SEPERATE REPORT
        else:
            for cid in i.comp_cbox:
                report = Report(client_id=i.client_id, companies=[cid], trans_obj=i.trans_obj, fiscal=i.fiscal)
                report.buildReport()
                reports.append(report)

            for did in i.div_cbox:
                report = Report(client_id=i.client_id, divisions=[did], trans_obj=i.trans_obj, fiscal=i.fiscal)
                report.buildReport()
                reports.append(report)
            
            for rid in i.reg_cbox:
                report = Report(client_id=i.client_id, regions=[rid], trans_obj=i.trans_obj, fiscal=i.fiscal)
                report.buildReport()
                reports.append(report)

            for aid in i.area_cbox:
                report = Report(client_id=i.client_id, areas=[aid], trans_obj=i.trans_obj, fiscal=i.fiscal)
                report.buildReport()
                reports.append(report)



        if i.trans_obj == 'acquisition':
            if i.export == 'PDF':
                html = jrender('/dashboard/acq_report_pdf.html', {'reports':reports})
                tmp = tempfile.TemporaryFile('w+b', prefix='tmp', suffix='.pdf')
                pdf = pisa.CreatePDF(str(html), tmp, '/var/www/webapps/static/')
                
                tmp.seek(0, 2)
                filesize = tmp.tell()
                tmp.seek(0)

                if pdf.err:
                    print 'PDF ERROR'
                if pdf.warn:
                    print 'WARNING'

                web.header('Content-Length', filesize)
                web.header('Content-Type', 'application/pdf')
                web.header('Content-Disposition', 'attachment; filename=%s' % 'Report.pdf')
                return tmp.read()

            if i.export == 'XLS':
                sheets = []
                for r in reports:
                    sheets.append(r.buildExcelData())

                xls = make_excel(sheets)

                xls.seek(0, 2)
                filesize = xls.tell()
                xls.seek(0)
                
                web.header('Content-Length', filesize)
                web.header('Content-Type', 'application/excel')
                web.header('Content-Disposition', 'attachment; filename=%s' % 'Report.xls')

                return xls.read()


                    


            return jrender('/dashboard/acq_report.html', {'reports':reports})
        else:
            return jrender('/dashboard/disp_report.html', {'reports':reports})

        


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

