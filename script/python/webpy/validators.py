
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
            return int(value)
        except:
            pass

def decimify(obj, name, value):
    """
    I convert a value to a decimal for storm
    """
    
    if value is not None:
        try:
            import decimal
            return decimal.Decimal(value)
        except:
            pass

def datify(obj, name, value):
    """
    I convert a value to a date
    """
    
    if value is not None:
        try:
            from datetime import date
            m, d, y = map(int, value.split('-'))
            return date(y, m, d)
        except:
            pass

def boolify(obj, name, value):
    """
    I convert a value to a Boolean for storm
    """
    
    if value is not None:
        try:
            if value in ['True', 'true', 't']:
                return True
            return False
        except:
            pass
