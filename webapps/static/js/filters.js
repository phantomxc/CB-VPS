
Filters = Class.create();

Filters.prototype = {

    initialize: function(baseElement) {
        
        this.element = $(baseElement);
        this.element.control = this;

        this.filds = [];
        this.constraints = {};

    },

    start: function() {
        this.clear();
    },

    addTypes: function(types) {
        types.each(function(obj) {
            this.constraints[obj['name']] = obj['constraints'];
        }.bind(this));
    },

    addFields: function(fields) {
        this.fields = fields; 
    },

    clear: function() {
        var tr = new Element('tr');
        var th = '<th></th><th></th><th>Criteria</th><th>Constraint</th><th>Value</th><th></th>';
        tr.update(th);
        this.element.update(tr);
        this.insert_row_after(this.addRow());
    },

    addRow: function() {
        var row = new Element('tr');
        row.control = this;

        //-----------------------
        // Add another constraint
        //-----------------------
        var plug_img = new Element('img', {'src':'/static/img/plus.jpg'});
        var td_add = new Element('td', {'class':'add_constraint'}).update(plug_img);

        td_add.observe('click', function(ev) {
            // insert new row
            this.control.insert_row_after(this.control.addRow(), this);
        }.bind(row));
        
        //-------------
        // Join
        //-------------
        var td_join = new Element('td', {'class':'join'});
        var join_button = new Element('input', {'type':'button'});
        join_button.setValue('AND');

        join_button.observe('click', function() {
            this.setValue(this.getValue() == 'AND' ? 'OR' : 'AND');
        });

        td_join.insert(join_button);
        row.join = join_button;

        //-------------
        // Field 
        //-------------
        var td_field = new Element('td');
        var select = new Element('select');
        var base_option = new Element('option', {'value':''}).update('(Choose a field)');
        select.insert(base_option);

        this.fields.each(function(field) {
            var option = new Element('option', {'value':field.imap}).update(field.name.stripTags());
            option.field_type = field.type;
            select.insert(option);
        });
        
        select.observe('change', row.fire.bind(row, 'filters:change'));
        
        td_field.update(select);
        row.field = select;

        //------------
        // Constraint
        //------------

        var td_constraint = new Element('td');
        var select = new Element('select');

        select.observe('change', row.fire.bind(row, 'filters:change'));
        td_constraint.update(select);
        row.constraint = select;


        //-----------
        // Arg
        //-----------

        var td_arg = new Element('td');
        var input = new Element('input', {'type':'text'});

        td_arg.insert(input);
        row.arg = input;

        //------------------
        // Remove Constraint
        //------------------
        var td_remove = new Element('td', {'class':'remove_constraint'}).update('[X]');
        td_remove.observe('click', function(ev) {
            this.control.removeRow(this);
        }.bind(row));



        //------------------------------------------
        // Update constraint based on field selected
        //------------------------------------------
        row.update_constraint = function(field_type) {
            var constraints = row.control.constraints[field_type];

            if (constraints && constraints.length) {
                this.constraint.update();
                
                constraints.each(function(cons) {
                    if (cons.value) {
                        var opt = new Element('option', {'value':cons.value}).update(cons.name);
                    } else {
                        var opt = new Element('option').update(cons.name);
                    }
                    opt.args = cons.args;
                    this.constraint.insert(opt);
                }.bind(this));
                this.constraint.show();
            } else {
                this.constraint.update();
                this.constraint.hide();
            }
        }.bind(row);

        row.updateArg = function(args) {
            if (args) {
                this.arg.show();
            } else {
                this.arg.hide();
            }
        }.bind(row);

        //-----------------------------
        // Watch changes in the row
        //-----------------------------

        row.observe('filters:change', function() {
            this.current_field_type = this.current_field_type || -1;

            // Did the field change?
            var new_field_type = this.field.childElements()[this.field.selectedIndex].field_type;

            // Display the correct set of constraint options
            if (this.current_field_type != new_field_type) {
                this.current_field_type = new_field_type;
                this.update_constraint(this.current_field_type);
            }

            // Display the appropriate number of args
            if (this.constraint.selectedIndex >= 0) {
                var args = this.constraint.childElements()[this.constraint.selectedIndex].args;
                this.updateArg(args);
            } else {
                this.updateArg(0);
            }

            // hide join if first row
            if (this.previousSiblings().length > 1) {
                this.join.show();
            } else {
                this.join.hide();
            }
            
        });
       
        // insert into the tr
        [td_add, td_join, td_field, td_constraint, td_arg, td_remove].each(function(obj) {
            row.insert(obj);
        });

        row.fire('filters:change');
        return row;
    },

    //--------------------------
    // Insert after specific row
    //--------------------------

    insert_row_after: function(row, after_who) {
        if (!after_who) {
            this.element.insert(row);
        } else {
            Element.insert(after_who, {after:row});
            after_who.fire('filters:change');
        }
        row.fire('filters:change');
    },

    removeRow: function(row) {
        var prevs = row.previousSiblings();
        var nexts = row.nextSiblings();

        if (prevs.length > 1 || nexts.length) {
            Element.remove(row);
        } else {
            this.clear();
        }

        if (prevs.length > 1) {
            prevs[0].fire('filters:change');
        }
        if (nexts.length) {
            nexts[0].fire('filters:change');
        }
    }

}  
