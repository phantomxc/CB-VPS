import xlwt
from StringIO import StringIO


def _lowerize(s):
    if hasattr(s, 'lower'):
        return s.lower()
    return s


def make_excel(sheets, stream=None):
    """
    Writes an excel file to 'stream'

    'sheets'  a single tuple or list of tuples representing sheets in the excell workbook.
              Each tuple can have 2 or 3 elements: (sheet_name, data_list, headers)

    'stream'     stream to which the data will be written. If none supplied, will write to
                a stringio and return the handle

    examples:

        make a single sheet with two rows and no headers

        make_excel(('sheet1', [[0,1,2,3,4],[5,6,7,8,9]]))

        make a single sheet with two rows and headers
        make_excel(('sheet1', [[1,2,3],[4,5,6]], ['a','b','c']))

        make a single sheet using dict data with headers
        data = [{'a':1, 'b':2, 'c':3},
                {'a':4, 'b':5, 'c':6}]
        make_excel(('sheet1', data, ['a', 'b', 'c']))
    """


    if stream is None:
        stream = StringIO()

    wkbk = xlwt.Workbook()

    if type(sheets) == tuple:
        sheets = [sheets]

    for sheet in sheets:
        name = ''
        data = []
        headers = []

        if len(sheet) == 2:
            name = sheet[0]
            data = sheet[1]
        elif len(sheet) == 3:
            name = sheet[0]
            data = sheet[1]
            headers = sheet[2]
        else:
            raise Exception('sheet tuples must be length 2 or 3')

        wksheet = wkbk.add_sheet(name)

        cur_row = 0

        header_dict = {}

        if headers:
            for i in xrange(0, len(headers)):
                header_dict[_lowerize(headers[i])] = i
                wksheet.write(cur_row, i, headers[i])

            cur_row += 1

        for row in data:
            if type(row) in [list, tuple]:
                for i in xrange(0, len(row)):
                    wksheet.write(cur_row, i, row[i])
            elif isinstance(row, dict):
                lrow = {}
                for k,v in row.items():
                    lrow[_lowerize(k)] = v
                if not header_dict:
                    raise Exception('Dictionary data requires a header row')

                for header_name, header_pos in header_dict.items():
                    val = lrow.get(header_name, '')
                    wksheet.write(cur_row, header_pos, val)
            cur_row += 1

    wkbk.save(stream)

    return stream
