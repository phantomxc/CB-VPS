import os
from jinja2 import Environment, FileSystemLoader

#-------------
# Environment
#-------------
template_root = '/var/www/webapps/templates'
JLOADER = FileSystemLoader(template_root, encoding='utf-8')
JENV = Environment(block_start_string='[[',
    block_end_string=']]',
    variable_start_string='[-',
    variable_end_string='-]',
    comment_start_string='[#',
    comment_end_string='#]',
    loader=JLOADER,
    extensions=[],
    cache_size=50,
)

JENV.add_extension('jinja2.ext.i18n')
JENV.add_extension('jinja2.ext.do')

def jrender(template_name, params=None):
    if params is None:
        params = {}

    return JENV.get_template(template_name).render(params)
        
