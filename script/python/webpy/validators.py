
def unicoder(obj, name, value):
    """
    I convert value to unicode for storm
    """
    if value is not None:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            ascii_text = str(value).encode('string_escape')
            return unicode(ascii_text)
    return value


def intify(obj, name, value):
    """
    I convert a value to an int for storm
    """

    if value is not None:
        try:
            if isinstance(value, int):
                return value
            if ',' in value:
                value = value.replace(',','')
            return int(value)
        except:
            print value
            print 'int boom'
            pass

def decimify(obj, name, value):
    """
    I convert a value to a decimal for storm
    """
    
    if value is not None:
        try:
            from decimal import Decimal as Dec
            value = str(value)
            return Dec(value)
        except:
            print 'dec boom'
            pass

def datify(obj, name, value):
    """
    I convert a value to a date
    """
    
    if value is not None:
        try:
            from datetime import date as mydate
            y, m, d = map(int, value.split('-'))
            return mydate(y, m, d)
        except:
            pass

def boolify(obj, name, value):
    """
    I convert a value to a Boolean for storm
    """
    
    if value is not None:
        try:
            if value in ['True', 'true', 't', True]:
                return True
            return False
        except:
            pass
