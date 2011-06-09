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
        return;
    },

    scriptifyFilters: function(li) {
        return;
    }

}

document.observe("dom:loaded", function(ev) {
    var page = new Dashboard();
});


