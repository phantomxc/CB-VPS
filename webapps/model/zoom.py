from webpy.dark import *
from storm.locals import *
import csv
from datetime import datetime

import sys
sys.stdout = sys.stderr

class Zoom(Storm):
    """
    I represent a zoomerang survey
    """
    __storm_table__ = "zoomerang"
    
    id = Int(primary=True)
    email = Unicode(validator=unicoder)
    sent_date = Date(validator=datify)
    submit_date = Date()
    avg_score = Int(validator=intify)
    client_id = Int(validator=intify)
    employee_id = Int(validator=intify)

    #References
    qa = ReferenceSet(id, 'ZoomQA.z_id')
    client = Reference(client_id, 'client.id')
    
    def __init__(self, store, survey):
        """
        Requires a web.py file object for the survey
        """

        # write the upload to a tmp file
        f = open('/tmp/' + survey.filename, "w")
        f.write(survey.file.read())
        f.close()
        #open the file in universal mode to fix zoomerangs errors
        data = list(csv.reader(open('/tmp/' + survey.filename, 'rU')))
        data = zip(*data)
        
        #create the object
        self.email = data[1][1]
        submit_date = datetime.strptime(data[2][1].split()[0], '%m/%d/%y')
        self.submit_date = submit_date
        store.add(self)
        store.commit()
        for res in data[3:16]:
            z = ZoomQA()
            z.question = res[0]
            z.answer = res[1]
            z.z_id = self.id
            store.add(z)
        store.commit()
         

class ZoomQA(Storm):
    """
    I join a survey to the questions and answers
    """
    __storm_table__ = "zoomqa"

    id = Int(primary=True)
    question = Unicode(validator=unicoder)
    answer = Unicode(validator=unicoder)
    z_id = Int()
