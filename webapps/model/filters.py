

#int [=, >, <, >=, <=, !=]

#text ['is', 'is not', 'contains']

#bool [True, False]



class FieldTypes(object):
    """
    I represent the filter types
    """

    def __init__(self):
    
        self.intField = {'name':'int', 'constraints':[]}

        self.textField = {'name':'text', 'constraints':[]}

        self.boolField = {'name':'bool', 'constraints':[]}

        self.dateField = {'name':'date', 'constraints':[]}

        self.intConstraints()
        self.textConstraints()
        self.boolConstraints()
        self.dateConstraints()
        


    def returnTypes(self):
        """
        return all the field types and corresponding constraints
        """
        
        self.types = [self.intField, self.textField, self.boolField, self.dateField]
        return self.types

    
    def intConstraints(self):
        """
        I am the int constraints
        """
        
        args = ['=', '>', '<', '>=', '<=', '!=']

        for a in args:
            self.intField['constraints'].append({'name':a, 'value':a, 'args':1})

    def textConstraints(self):
        """
        I am the text constraints
        """

        args = {
            'is':{'value':'=='},
            'is not':{'value':'!='},
            'contains':{'value':'contains'}
        }

        for a in args.keys():
            self.textField['constraints'].append({'name':a, 'value':args[a]['value'], 'args':1})

    def boolConstraints(self):
        """
        I am the bool constraints
        """

        args = ['True','False']

        for a in args:
            self.boolField['constraints'].append({'name':a, 'args':0})

    def dateConstraints(self):
        """
        I am the date constrains
        """
        
        args = {
            'is not set':{'value':'is null', 'args':0},
            'is set':{'value':'is not null', 'args':0},
            'is':{'value':'==', 'args':1},
            'is before':{'value':'<', 'args':1},
            'on or before':{'value':'<=', 'args':1},
            'is after':{'value':'>', 'args':1},
            'on or after':{'value':'>=', 'args':1}
        }

        for a in args.keys():
            self.dateField['constraints'].append({'name':a, 'value':args[a]['value'], 'args':args[a]['args']})
