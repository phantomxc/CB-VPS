Transactions = Class.create();
Transactions.prototype = {
    initialize: function() {
        // Build Transaction tabs. 
        var tabs = new Tabs('tab_container');
        this.tabs = tabs;
        this.tabs.t1 = tabs.addTab('Add Transaction', 'add_trans', '', function(){return{};}, this.scriptifyAddTrans.bind(this));
        this.tabs.t2 = tabs.addTab('Edit Transactions', 'edit_trans');
        this.tabs.t3 = tabs.addTab('Metrics', 'metrics');
        this.tabs.t4 = tabs.addTab('Properties', 'properties');
        this.tabs.start(this.tabs.t1);
    },

    populateForm: function(base, next, url, sel) {
        //---------------
        // Build select boxes based on the field selected
        //
        // base: item id to build the rest of the info off
        // next: next id to build
        // url: url to get required information
        // sel: optional for the starting select
        //---------------
        if (sel) {
            var select = sel
        } else {
            var select = $(base).select('[class="select"]')[0];
        }

        if (next == 'none') {
            return;
        }
        $(select).observe('change', function(ev) {
            basevar = $(select).getValue();
            new Ajax.Request(url, {
                method:'POST',
                parameters: {
                    'id':basevar
                },
                onSuccess: function(res) {
                    iter = res.responseJSON;
                    var sel = new Element('select', {'name':next});
                    sel.insert(new Element('option').insert('Select One'));
                    iter.each(function(k) {
                        var opt = new Element('option', {'value':k.id});
                        opt.insert(k.title);
                        sel.insert(opt);
                    });

                    $(next).next().update(sel);
                    
                    this.populateForm(next, $(next).readAttribute('next'), $(next).readAttribute('ajax'), sel);
                }.bind(this)
            });

            $(next).next().update('Loading');
        }.bind(this));
    },

    scriptifyAddTrans: function() {
        // Add Transaction tab processor
        this.watchClient();
        this.propertySearch();
        this.newProperty();
        this.buildTransactionView();
    },

    buildTransactionView: function() {
        // Show different form fields based on the transaction type
        $('trans_type').observe('change', function(ev) {
            new Ajax.Request('get_trans_details', {
                method:'POST',
                parameters: {'type':$('trans_type').getValue()},
                onSuccess:  function(res) {
                    $('trans_details').update(res.responseText);
                }
            });
            $('trans_details').update('Loading...');
        });
    },

    watchClient: function() {
        // Start the drop down generation based on client selected
        var base = 'cid';
        var next = $(base).readAttribute('next');
        var url = $(base).readAttribute('ajax');
        this.populateForm(base, next, url, '');
    },

    propertySearch: function() {
        // start the ajax autocomplete object
        a = new Autocomplete('property_query', {
            serviceUrl:'propertysearch/',
            minChars:2,
            onSelect: function(value, data) {
                $('property_search_result').setValue(data);
            }
        });

        a.initialize();
    },

    newProperty: function() {
        // Create a new proptery if it doesn't exist in the database
        $('new_property').observe('click', function(ev) {
            $('new_property_table').show();
            $('property_search').hide();
        });
    }

}

document.observe("dom:loaded", function(ev) {
    var page = new Transactions();
});


