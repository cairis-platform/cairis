# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1430304962.133159
_enable_loop = True
_template_filename = '/home/TChosenOne/Documents/CAIRIS-web/cairis/cairis/templates/common.error.mako'
_template_uri = 'common.error.mako'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        msg = context.get('msg', UNDEFINED)
        code = context.get('code', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\n<html>\n<head lang="en">\n    <meta charset="UTF-8">\n    <title>')
        __M_writer(unicode(code))
        __M_writer(u' ')
        __M_writer(unicode(title))
        __M_writer(u' | CAIRIS</title>\n    <meta content=\'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\' name=\'viewport\'>\n    <!-- Bootstrap 3.3.2 -->\n    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />\n    <style type="text/css">\n        body {\n            background: #EEE;\n        }\n        .container {\n            background: #FFF;\n            padding-bottom: 48pt;\n        }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div>\n            <h1>')
        __M_writer(unicode(code))
        __M_writer(u' ')
        __M_writer(unicode(title))
        __M_writer(u'</h1>\n            <p>')
        __M_writer(unicode(msg))
        __M_writer(u'</p>\n        </div>\n        <div>\n            <p><a href="/">Back to home</a></p>\n        </div>\n    </div>\n    <!-- jQuery 2.1.3 -->\n    <script src="/static/plugins/jQuery/jQuery-2.1.3.min.js"></script>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"32": 23, "33": 23, "39": 33, "15": 0, "23": 1, "24": 5, "25": 5, "26": 5, "27": 5, "28": 22, "29": 22, "30": 22, "31": 22}, "uri": "common.error.mako", "filename": "/home/TChosenOne/Documents/CAIRIS-web/cairis/cairis/templates/common.error.mako"}
__M_END_METADATA
"""
