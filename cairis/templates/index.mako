<!DOCTYPE html>
<html>
<head lang="en">

    <meta charset="UTF-8">
    <title>${title}</title>
    <meta content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' name='viewport'>
    <!-- Bootstrap 3.3.2 -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <!-- Font Awesome Icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons -->
    <link href="http://code.ionicframework.com/ionicons/2.0.0/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <link href="dist/css/AdminLTE.min.css" rel="stylesheet" type="text/css" />
    <!-- AdminLTE Skins. We have chosen the skin-blue for this starter
          page. However, you can choose any other skin. Make sure you
          apply the skin class to the body tag so the changes take effect.
    -->
    <link href="dist/css/skins/skin-blue.min.css" rel="stylesheet" type="text/css" />

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
</head>
<body class="skin-blue">
<div class="wrapper">

    <!-- Main Header -->
    <header class="main-header">

        <!-- Logo -->
        <a href="#" class="logo">CAIRIS</a>

        <!-- Header Navbar -->
        <nav class="navbar navbar-static-top" role="navigation">
            <!-- Sidebar toggle button-->
            <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
                <span class="sr-only">Toggle navigation</span>
            </a>
            <!-- Navbar Right Menu -->
            <div class="navbar-custom-menu">
                <ul class="nav navbar-nav">
                    <!-- Messages: style can be found in dropdown.less-->
                    <!-- Tasks Menu -->
                    <li class="dropdown tasks-menu">
                        <!-- Menu Toggle Button -->
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <i class="fa fa-flag-o"></i>
                            <span class="label label-danger">9</span>
                        </a>
                        <ul class="dropdown-menu">
                            <li class="header">You have 9 tasks</li>
                            <li>
                                <!-- Inner menu: contains the tasks -->
                                <ul class="menu">
                                    <li><!-- Task item -->
                                        <a href="#">
                                            <!-- Task title and progress text -->
                                            <h3>
                                                Design some buttons
                                                <small class="pull-right">20%</small>
                                            </h3>
                                            <!-- The progress bar -->
                                            <div class="progress xs">
                                                <!-- Change the css width attribute to simulate progress -->
                                                <div class="progress-bar progress-bar-aqua" style="width: 20%" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                                                    <span class="sr-only">20% Complete</span>
                                                </div>
                                            </div>
                                        </a>
                                    </li><!-- end task item -->
                                </ul>
                            </li>
                            <li class="footer">
                                <a href="#">View all tasks</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </nav>
    </header>

    <aside class="main-sidebar">
        <!-- sidebar - sidebar.less -->
        <section class="sidebar">
            <div id="sidebar-scrolling">
            <ul class="sidebar-menu">
                <li class="header">MENU</li>
                <!-- Optionally, you can add icons to the links -->
                % for nav in navList:
                % if hasattr(nav, 'navObjects'):
                <li class="treeview">
                    <a href="${nav.href}">${printIcon(nav)}<span>${nav.text}</span><i class="fa fa-angle-left pull-right"></i>
                    </a>
                    <ul class="treeview-menu">
                        ${innerTree(navObjects=nav.navObjects)}
                    </ul>
                </li>
                % else:
                <li><a href="${nav.href}">${printIcon(nav)}<span>${nav.text}</span>
                </a></li>
                %endif
                % endfor
            </ul>
            </div>
        </section>
    </aside>

    <!-- Content Wrapper. Contains page content -->
    <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        <section class="content-header">
            <h1>
                Page Header
                <small>Optional description</small>
            </h1>
            <ol class="breadcrumb">
                <li><a href="#"><i class="fa fa-dashboard"></i> Level</a></li>
                <li class="active">Here</li>
            </ol>
        </section>
        <!-- Main content -->
        <section class="content">
            <!-- Your Page Content Here -->

            ${body}

        </section><!-- /.content -->
    </div><!-- /.content-wrapper -->

    <!-- rightnav -->
    <div id="rightnavGear" class="no-print"
         style="position: fixed; top: 100px; right: 0px; border-radius: 5px 0px 0px 5px; padding: 10px 15px; font-size: 16px; z-index: 99999; cursor: pointer; color: rgb(60, 141, 188); box-shadow: rgba(0, 0, 0, 0.0980392) 0px 1px 3px; background: rgb(255, 255, 255);">
        <i class="fa fa-gear"></i></div>
    <div id="rightnavMenu" class="no-print"
         style="padding: 10px; position: fixed; top: 100px; right: -250px; border: 0px solid rgb(221, 221, 221); width: 250px; z-index: 99999; box-shadow: rgba(0, 0, 0, 0.0980392) 0px 1px 3px; background: rgb(255, 255, 255);">
        <h4 class="text-light-blue" style="margin: 0 0 5px 0; border-bottom: 1px solid #ddd; padding-bottom: 15px;">
            Options</h4>
    </div>
    <footer class="main-footer">
        <!-- To the right -->
        <div class="pull-right hidden-xs">
            Anything you want
        </div>
        <!-- Default to the left -->
        <strong>Copyright &copy; 2015 <a href="#">Company</a>.</strong> All rights reserved.
    </footer>

</div>
<!-- REQUIRED JS SCRIPTS -->
<!-- jQuery 2.1.3 -->
<script src="plugins/jQuery/jQuery-2.1.3.min.js"></script>
<!-- Bootstrap 3.3.2 JS -->
<script src="bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
<!-- AdminLTE App -->
<script src="dist/js/app.min.js" type="text/javascript"></script>
<!-- Slimscroll App  -->
<script src="plugins/slimScroll/jquery.slimscroll.js" type="text/javascript"></script>
<!-- Script for the right nav -->
<script>
    $(document).ready(function(){
        $('#rightnavGear').click(function(){
            var navGear = $('#rightnavGear');
            var navMenu = $('#rightnavMenu');
            if (!navGear.hasClass("open")) {
                navGear.animate({"right": "250px"});
                navMenu.animate({"right": "0"});
                navGear.addClass("open");
            } else {
                navGear.animate({"right": "0"});
                navMenu.animate({"right": "-250px"});
                navGear.removeClass("open");
            }
        });
    });
</script>
<script>
    $(window).load(function(){
        $('#sidebar-scrolling').slimScroll({
            height: $('.main-sidebar').height() - 20
        });
    });
</script>
</body>
</html>
<%def name="innerTree(navObjects)">
% for row in navObjects:
<li><a href="${row.href}">${row.text}
</a></li>
% endfor
</%def>
<%def name="printIcon(nav)">
% if hasattr(nav, 'icon'):
<i class='${nav.icon}'></i>
% endif
</%def>