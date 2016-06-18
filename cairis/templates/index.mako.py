# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1434060690.119963
_enable_loop = True
_template_filename = '/home/cairisuser/CAIRIS-web/cairis/cairis/templates/index.mako'
_template_uri = 'index.mako'
_source_encoding = 'ascii'
_exports = ['innerTree', 'printIcon']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        body = context.get('body', UNDEFINED)
        title = context.get('title', UNDEFINED)
        def printIcon(nav):
            return render_printIcon(context.locals_(__M_locals),nav)
        def innerTree(navObjects):
            return render_innerTree(context.locals_(__M_locals),navObjects)
        navList = context.get('navList', UNDEFINED)
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\r\n<html>\r\n<head lang="en">\r\n\r\n    <meta charset="UTF-8">\r\n    <title>')
        # SOURCE LINE 6
        __M_writer(unicode(title))
        __M_writer(u'</title>\r\n    <meta content=\'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\' name=\'viewport\'>\r\n    <!-- Bootstrap 3.3.2 -->\r\n    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />\r\n    <!-- Font Awesome Icons -->\r\n    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />\r\n    <!-- Ionicons -->\r\n    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />\r\n    <!-- Theme style -->\r\n    <link href="dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />\r\n    <!-- AdminLTE Skins. We have chosen the skin-blue for this starter\r\n          page. However, you can choose any other skin. Make sure you\r\n          apply the skin class to the body tag so the changes take effect.\r\n    -->\r\n    <link href="dist/css/skins/skin-blue.min.css" rel="stylesheet" type="text/css" />\r\n\r\n    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->\r\n    <!-- WARNING: Respond.js doesn\'t work if you view the page via file:// -->\r\n    <!--[if lt IE 9]>\r\n    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>\r\n    <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>\r\n    <![endif]-->\r\n</head>\r\n<body class="skin-blue">\r\n<div class="wrapper">\r\n\r\n    <!-- Main Header -->\r\n    <header class="main-header">\r\n\r\n        <!-- Logo -->\r\n        <a href="#" class="logo">CAIRIS</a>\r\n\r\n        <!-- Header Navbar -->\r\n        <nav class="navbar navbar-static-top" role="navigation">\r\n            <!-- Sidebar toggle button-->\r\n            <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">\r\n                <span class="sr-only">Toggle navigation</span>\r\n            </a>\r\n            <!-- Navbar Right Menu -->\r\n            <div class="navbar-custom-menu">\r\n                <ul class="nav navbar-nav">\r\n                    <!-- Messages: style can be found in dropdown.less-->\r\n                    <!-- Tasks Menu -->\r\n                    <li class="dropdown tasks-menu">\r\n                        <!-- Menu Toggle Button -->\r\n                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">\r\n                            <i class="fa fa-flag-o"></i>\r\n                            <span class="label label-danger">9</span>\r\n                        </a>\r\n                        <ul class="dropdown-menu">\r\n                            <li class="header">You have 9 tasks</li>\r\n                            <li>\r\n                                <!-- Inner menu: contains the tasks -->\r\n                                <ul class="menu">\r\n                                    <li><!-- Task item -->\r\n                                        <a href="#">\r\n                                            <!-- Task title and progress text -->\r\n                                            <h3>\r\n                                                Design some buttons\r\n                                                <small class="pull-right">20%</small>\r\n                                            </h3>\r\n                                            <!-- The progress bar -->\r\n                                            <div class="progress xs">\r\n                                                <!-- Change the css width attribute to simulate progress -->\r\n                                                <div class="progress-bar progress-bar-aqua" style="width: 20%" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">\r\n                                                    <span class="sr-only">20% Complete</span>\r\n                                                </div>\r\n                                            </div>\r\n                                        </a>\r\n                                    </li><!-- end task item -->\r\n                                </ul>\r\n                            </li>\r\n                            <li class="footer">\r\n                                <a href="#">View all tasks</a>\r\n                            </li>\r\n                        </ul>\r\n                    </li>\r\n                </ul>\r\n            </div>\r\n        </nav>\r\n    </header>\r\n\r\n    <aside class="main-sidebar">\r\n        <!-- sidebar - sidebar.less -->\r\n        <section class="sidebar">\r\n            <div id="sidebar-scrolling">\r\n            <ul class="sidebar-menu">\r\n                <li class="header">MENU</li>\r\n                <!-- Optionally, you can add icons to the links -->\r\n')
        # SOURCE LINE 95
        for nav in navList:
            # SOURCE LINE 96
            if hasattr(nav, 'navObjects'):
                # SOURCE LINE 97
                __M_writer(u'                <li class="treeview">\r\n                    <a href="')
                # SOURCE LINE 98
                __M_writer(unicode(nav.href))
                __M_writer(u'">')
                __M_writer(unicode(printIcon(nav)))
                __M_writer(u'<span>')
                __M_writer(unicode(nav.text))
                __M_writer(u'</span><i class="fa fa-angle-left pull-right"></i>\r\n                    </a>\r\n                    <ul class="treeview-menu">\r\n                        ')
                # SOURCE LINE 101
                __M_writer(unicode(innerTree(navObjects=nav.navObjects)))
                __M_writer(u'\r\n                    </ul>\r\n                </li>\r\n')
                # SOURCE LINE 104
            else:
                # SOURCE LINE 105
                __M_writer(u'                <li><a href="')
                __M_writer(unicode(nav.href))
                __M_writer(u'">')
                __M_writer(unicode(printIcon(nav)))
                __M_writer(u'<span>')
                __M_writer(unicode(nav.text))
                __M_writer(u'</span>\r\n                </a></li>\r\n')
                pass
            pass
        # SOURCE LINE 109
        __M_writer(u'            </ul>\r\n            </div>\r\n        </section>\r\n    </aside>\r\n\r\n    <!-- Content Wrapper. Contains page content -->\r\n    <div class="content-wrapper">\r\n        <!-- Content Header (Page header) -->\r\n        <section class="content-header">\r\n            <h1>\r\n                Page Header\r\n                <small>Optional description</small>\r\n            </h1>\r\n            <ol class="breadcrumb">\r\n                <li><a href="#"><i class="fa fa-dashboard"></i> Level</a></li>\r\n                <li class="active">Here</li>\r\n            </ol>\r\n        </section>\r\n        <!-- Main content -->\r\n        <section class="content">\r\n            <!-- Your Page Content Here -->\r\n\r\n            ')
        # SOURCE LINE 131
        __M_writer(unicode(body))
        __M_writer(u'\r\n\r\n        </section><!-- /.content -->\r\n    </div><!-- /.content-wrapper -->\r\n\r\n    <!-- rightnav -->\r\n    <div id="rightnavGear" class="no-print"\r\n         style="position: fixed; top: 100px; right: 0px; border-radius: 5px 0px 0px 5px; padding: 10px 15px; font-size: 16px; z-index: 99999; cursor: pointer; color: rgb(60, 141, 188); box-shadow: rgba(0, 0, 0, 0.0980392) 0px 1px 3px; background: rgb(255, 255, 255);">\r\n        <i class="fa fa-gear"></i></div>\r\n    <div id="rightnavMenu" class="no-print"\r\n         style="padding: 10px; position: fixed; top: 100px; right: -250px; border: 0px solid rgb(221, 221, 221); width: 250px; z-index: 99999; box-shadow: rgba(0, 0, 0, 0.0980392) 0px 1px 3px; background: rgb(255, 255, 255);">\r\n        <h4 class="text-light-blue" style="margin: 0 0 5px 0; border-bottom: 1px solid #ddd; padding-bottom: 15px;">\r\n            Options</h4>\r\n    </div>\r\n    <footer class="main-footer">\r\n        <!-- To the right -->\r\n        <div class="pull-right hidden-xs">\r\n            Anything you want\r\n        </div>\r\n        <!-- Default to the left -->\r\n        <strong>Copyright &copy; 2015 <a href="#">Company</a>.</strong> All rights reserved.\r\n    </footer>\r\n\r\n</div>\r\n<!-- REQUIRED JS SCRIPTS -->\r\n<!-- jQuery 2.1.3 -->\r\n<script src="plugins/jQuery/jQuery-2.1.3.min.js"></script>\r\n<!-- Bootstrap 3.3.2 JS -->\r\n<script src="bootstrap/js/bootstrap.min.js" type="text/javascript"></script>\r\n<!-- AdminLTE App -->\r\n<script src="dist/js/app.min.js" type="text/javascript"></script>\r\n<!-- Slimscroll App  -->\r\n<script src="plugins/slimScroll/jquery.slimscroll.js" type="text/javascript"></script>\r\n<!-- Script for the right nav -->\r\n<script>\r\n    $(document).ready(function(){\r\n        $(\'#rightnavGear\').click(function(){\r\n            var navGear = $(\'#rightnavGear\');\r\n            var navMenu = $(\'#rightnavMenu\');\r\n            if (!navGear.hasClass("open")) {\r\n                navGear.animate({"right": "250px"});\r\n                navMenu.animate({"right": "0"});\r\n                navGear.addClass("open");\r\n            } else {\r\n                navGear.animate({"right": "0"});\r\n                navMenu.animate({"right": "-250px"});\r\n                navGear.removeClass("open");\r\n            }\r\n        });\r\n    });\r\n</script>\r\n<script>\r\n    $(window).load(function(){\r\n        $(\'#sidebar-scrolling\').slimScroll({\r\n            height: $(\'.main-sidebar\').height() - 20\r\n        });\r\n    });\r\n</script>\r\n</body>\r\n</html>\r\n')
        # SOURCE LINE 196
        __M_writer(u'\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_innerTree(context,navObjects):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 191
        __M_writer(u'\r\n')
        # SOURCE LINE 192
        for row in navObjects:
            # SOURCE LINE 193
            __M_writer(u'<li><a href="')
            __M_writer(unicode(row.href))
            __M_writer(u'">')
            __M_writer(unicode(row.text))
            __M_writer(u'\r\n</a></li>\r\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_printIcon(context,nav):
    __M_caller = context.caller_stack._push_frame()
    try:
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 197
        __M_writer(u'\r\n')
        # SOURCE LINE 198
        if hasattr(nav, 'icon'):
            # SOURCE LINE 199
            __M_writer(u"<i class='")
            __M_writer(unicode(nav.icon))
            __M_writer(u"'></i>\r\n")
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


