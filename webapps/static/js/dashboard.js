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
        this.rtabs.t1 = rtabs.addTab('Companies', 'companies', 'companies', function(){ return{};}, this.scriptifyCompanies.bind(this));
        this.rtabs.t2 = rtabs.addTab('Filters', 'filters', 'filters', this.buildGlobals.bind(this), this.scriptifyFilters.bind(this));

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

        content.select('input.cbox').each(function(cbox) {
            cbox.observe('click', function(ev) {
                var col_div = this.up(1).next();
                col_div.select('input.cbox').each(function(child_boxes) {
                    child_boxes.checked = true;
                });
            });
        });
    },

    setupForm: function() {
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
        return;
    }

}

document.observe("dom:loaded", function(ev) {
    var page = new Dashboard();
});


