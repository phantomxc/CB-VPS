<html>
    <head>
        <title>CRE Dashboard</title>
        <link rel="stylesheet" type="text/css" href="../static/css/main.css" />
        <script src="../static/js/prototype.js" type="text/javascript"></script>
        <script src="../static/js/scriptaculous.js" type="text/javascript"></script>
        <script src="../static/js/raphael-min.js" type="text/javascript"></script>
        <script src="../static/js/g.raphael-min.js" type="text/javascript"></script>
        <script src="../static/js/g.pie-min.js" type="text/javascript"></script>
        <script src="../static/js/collapsables.js" type="text/javascript"></script>
        <script src="../static/js/dashboard.js" type="text/javascript"></script>
    </head>
    <body>
        <div id="base_container">
            <div id="header_container">
                <span class="title">Company Name </span> <span id="cre_title"> - CRE Dashboard</span>
            </div>
            <div id="menu">
                <?php
                    include("menu/main.php");
                ?>
            </div>
            <div id="content_container">
                <table id="main_content">
                    <tr>
                        <td id="content_left">
                            <div id="graph">
<script type="text/javascript" charset="utf-8">
            window.onload = function () {
                var r = Raphael("graph");
                r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
                
                r.g.text(320, 50, "Property Chart").attr({"font-size": 20});
                
                var pie = r.g.piechart(320, 230, 100, [55, 20, 13, 32, 5, 1, 2, 10], {legend: ["%%.%% - Enterprise Users", "IE Users"], legendpos: "west", href: ["http://raphaeljs.com", "http://g.raphaeljs.com"]});
                pie.hover(function () {
                    this.sector.stop();
                    this.sector.scale(1.1, 1.1, this.cx, this.cy);
                    if (this.label) {
                        this.label[0].stop();
                        this.label[0].scale(1.5);
                        this.label[1].attr({"font-weight": 800});
                    }
                }, function () {
                    this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
                    if (this.label) {
                        this.label[0].animate({scale: 1}, 500, "bounce");
                        this.label[1].attr({"font-weight": 400});
                    }
                });
                
            };
        </script>

                            </div>
                        </td>
                        <td id="content_right" valign="top">
                            <div id="floatmenu"></div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
</html>

