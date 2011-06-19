Dashboard = Class.create();
Dashboard.prototype = {
    initialize: function() {
        //---------------------------
        // Start the Dashboard class
        //---------------------------

        // LEFT TABS
        var ltabs = new Tabs('left_tabs');
        this.ltabs = ltabs;
        this.ltabs.t1 = ltabs.addTab('Acquisitions', 'acq', '', function() {return{};}, this.scriptifyAcquisitions.bind(this));
        this.ltabs.t2 = ltabs.addTab('Dispositions', 'disp', '', function() {return{};}, this.scriptifyDispositions.bind(this));
        this.ltabs.t3 = ltabs.addTab('Graphs', 'graphs');

        this.ltabs.loadingdiv = $('lloading');

        var rtabs = new Tabs('right_tabs');
        this.rtabs = rtabs;
        this.rtabs.t1 = rtabs.addTab('Companies', 'companies');
        this.rtabs.t2 = rtabs.addTab('Filters', 'filters_container', '', function() {return{};}, this.scriptifyFilters.bind(this));

        this.rtabs.loadingdiv = $('rloading');

        this.globalParams = {};

        // chooseTab Wrap
        this.ltabs.chooseTab = this.ltabs.chooseTab.wrap(
            function(func, arg) {
                this.globalParams['left_active_tab'] = arg.innerHTML;
                return func(arg);
            }.bind(this));
        
        this.rtabs.chooseTab = this.rtabs.chooseTab.wrap(
            function(func, arg) {
                this.globalParams['right_active_tab'] = arg.innerHTML;
                return func(arg);
            }.bind(this));

        // START THE TABS
        this.rtabs.start(this.rtabs.t1);
        this.ltabs.start(this.ltabs.t1);

        $('disp_filters').hide();

        new Ajax.Request('companies', {
            method:'POST',
            parameters: this.globalParams,
            onSuccess: function(resp) {
                var li = new Element('li');
                li.content = $('companies');
                $('companies').update(resp.responseText);
                this.scriptifyCompanies(li);
            }.bind(this)
        });

        $('companies').update('Loading');
    },

    buildGlobals: function() {
    //---------------------------------------------------------------
    // Parameters to be passed to all tabs when a tab change happens.
    //---------------------------------------------------------------
        var params = {};
        for (key in this.globalParams) {
            if (!params[key]) {
                params[key] = this.globalParams[key];
            }
        }
        return params;
    },

    // SCRIPTIFY LEFT TABS
    scriptifyAcquisitions: function(li) {
        // If filters tab is active, reload
        if (this.rtabs.chosen == this.rtabs.t2) {
            this.rtabs.chooseTab(this.rtabs.t2);
        }
    },
    scriptifyDispositions: function(li) {
        // If filters tab is active, reload
        if (this.rtabs.chosen == this.rtabs.t2) {
            this.rtabs.chooseTab(this.rtabs.t2);
        }
    
    },

    // SCRIPTIFY RIGHT TABS
    scriptifyCompanies: function(li) {
        this.collapsables(li.content);    
        this.setupForm();

        // build the selected client default report
        this.defaultReport(this.globalParams['client_id']);


    },
    defaultReport: function(client_id) {
        var act = (this.ltabs.chosen == this.ltabs.t1) ? 'acquisition': 'disposition';
        new Ajax.Request('default_report', {
            method:'POST',
            parameters:{'client_id':client_id, 'trans_obj':act},
            onSuccess: function(resp) {
                if (this.ltabs.chosen == this.ltabs.t1) {
                    $('acq').update(resp.responseText);
                } else {
                    $('disp').update(resp.responseText);
                }
            }.bind(this),
            onFailure: function(ev) {
                alert('error');
            }
        });
    },
    // Make the companies tab collapsables
    collapsables: function(content) {
        // start the collapsable containers hidden
        content.select('div.collapsable').each(function(container) {
            container.hide();   
        });
        // observe clicking on the arrow, show children
        content.select('span.coll_arrows').each(function(coll) {
            coll.observe('click', function(ev) {
                var child_div = this.up().next();
                if (child_div.visible()) {
                    child_div.hide();
                    this.removeClassName('open');
                    this.addClassName('closed');
                } else {
                    child_div.show();
                    this.removeClassName('closed');
                    this.addClassName('open');
                }
            });
        });

// I don't think I want this auto child select. Its annoying
//
//        content.select('input.cbox').each(function(cbox) {
//            cbox.observe('click', function(ev) {
//                var col_div = this.up(1).next();
//                col_div.select('input.cbox').each(function(child_boxes) {
//                    child_boxes.checked = true;
//                });
//            });
//        });
    },

    setupForm: function() {
        var active_client = $('active_client_id').getValue();
        this.globalParams['client_id'] = active_client;
        Event.observe('dashboard_form', 'submit', function(event) {
            var act = (this.ltabs.chosen == this.ltabs.t1) ? 'acquisition': 'disposition';
            var act_div = (this.ltabs.chosen == this.ltabs.t1) ? $('acq') : $('disp');
            $('dashboard_form').request({
                parameters: {'trans_obj':act},
                onSuccess: function(res) {
                    act_div.update(res.responseText);
                }
            });
            act_div.update('Loading');
            
            Event.stop(event);
        }.bind(this));
    },

    scriptifyFilters: function(li) {
        // Determine Filter view
        if (this.ltabs.chosen == this.ltabs.t1) {
            $('acq_filters').show();
            $('disp_filters').hide();
        } 
        else if (this.ltabs.chosen == this.ltabs.t2) {
            $('acq_filters').hide();
            $('disp_filters').show();
        }
    }

}


function buildFilters(types) {
    var fields = [ {'name':'Old SQFT', 'imap':'old', 'type':'int'}, {'name':'Market Survey', 'imap':'mksvy','type':'bool'},
        {'name':'Survey Date', 'imap':'survey_date', 'type':'date'},
        {'name':'Notes', 'imap':'notes', 'type':'text'}
    ]
    
    var acq_filters = new Filters('acq_filter_table');
    acq_filters.addTypes(types);
    acq_filters.addFields(fields);
    acq_filters.start();

    var disp_filters = new Filters('disp_filter_table');
    disp_filters.addTypes(types);
    disp_filters.addFields(fields);
    disp_filters.start();
}

document.observe("dom:loaded", function(ev) {
    this.types = '';
    var page = new Dashboard();
    

    new Ajax.Request('filter_types', {
        method:'GET',
        onSuccess: function(resp) {
            this.types = resp.responseJSON;
            buildFilters(this.types);
        }.bind(this)
    });
});


