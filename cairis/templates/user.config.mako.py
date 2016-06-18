# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1430834205.12728
_enable_loop = True
_template_filename = '/home/TChosenOne/Documents/CAIRIS-web/cairis/cairis/templates/user.config.mako'
_template_uri = 'user.config.mako'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        action_url = context.get('action_url', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\n<html>\n<head lang="en">\n    <meta charset="UTF-8">\n    <title>Configuration | CAIRIS</title>\n    <meta content=\'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\' name=\'viewport\'>\n    <!-- Bootstrap 3.3.2 -->\n    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>\n</head>\n<body>\n<div class="col-md-4 col-md-offset-3">\n    <h1>Configuration</h1>\n\n    <div>\n        <form action="')
        __M_writer(unicode(action_url))
        __M_writer(u'" method="post" enctype="text/html" class="form-horizontal" role="form">\n            <div class="form-group">\n                <label for="host" class="control-label col-sm-2">Host:</label>\n                <div class="col-sm-10">\n                    <input type="text" id="host" name="host" value="127.0.0.1" class="form-control"/>\n                </div>\n            </div>\n            <div class="form-group">\n                <label for="port" class="control-label col-sm-2">Port:</label>\n                <div class="col-sm-10">\n                    <input type="text" id="port" name="port" value="3306" class="form-control"/>\n                </div>\n            </div>\n            <div class="form-group">\n                <label for="user" class="control-label col-sm-2">User:</label>\n                <div class="col-sm-10">\n                    <input type="text" id="user" name="user" value="cairis" class="form-control"/>\n                </div>\n            </div>\n            <div class="form-group">\n                <label for="passwd" class="control-label col-sm-2">Password:</label>\n                <div class="col-sm-10">\n                    <input type="password" id="passwd" name="passwd" value="cairis123" class="form-control"/>\n                </div>\n            </div>\n            <div class="form-group">\n                <label for="db" class="control-label col-sm-2">DB:</label>\n                <div class="col-sm-10">\n                    <input type="text" id="db" name="db" value="cairis" class="form-control"/>\n                </div>\n            </div>\n            <div class="form-group">\n                <div class="col-sm-10 col-sm-offset-2 checkbox">\n                    <label>\n                        <input type="checkbox" id="jsonPrettyPrint" name="jsonPrettyPrint" />JSON pretty printing\n                    </label>\n                </div>\n            </div>\n            <div class="form-group">\n                <div class="col-sm-10 col-sm-offset-2">\n                    <input type="submit" class="btn btn-primary" />\n                </div>\n            </div>\n        </form>\n    </div>\n</div>\n<script src="/static/plugins/jQuery/jQuery-2.1.3.min.js"></script>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"23": 15, "29": 23, "21": 1, "22": 15, "15": 0}, "uri": "user.config.mako", "filename": "/home/TChosenOne/Documents/CAIRIS-web/cairis/cairis/templates/user.config.mako"}
__M_END_METADATA
"""
