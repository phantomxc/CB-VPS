
collapsables = Class.create();
collapsables.prototype = {
    
    initialize: function(baseElement) {
        this.baseElement = $(baseElement);
    },

    addRow: function(title, url, params) {
        var c = {};
        c.title = Element('div').insert(title);
        c.container = Element('div', {'class':'rowContainer'});
        
        c.container.insert(c.title);
 
        c.content = this.addContent(c.container);
        c.url = url;
        c.params = params || {};
        c.title.observe('click', function(ev) {
            this.chooseRow(c)
        }.bind(this));
       
        this.baseElement.insert(c.container);
        if (this.baseElement.childElements().length == 1) {
            this.chosen = c;
            this.chooseRow(c);
        } else {
            this.makeDormant(c);
        }
        
    },
    
    addContent: function(container) {
        var content = Element('div', {'class':'content', 'style':'display:none'});
        container.insert(content);
        return content;
         
    },
    chooseRow: function(c) {
        if((this.chosen) && (this.chosen != c)) {
            this.chosen.title.removeClassName('active_title');
            this.chosen.title.addClassName('dormant_title');
            this.makeDormant(this.chosen);
        }
        if((this.chosen == c) && (this.baseElement.childElements().length > 1)) {
            return;
        };
        this.chosen = c;
        c.title.removeClassName('dormant_title');
        c.title.addClassName('active_title');
        
        this.rowChosen(c);
         
    },
    
    makeDormant: function(c) {
        Effect.BlindUp(c.content, {'duration':1});
        c.title.removeClassName('active_title');
        c.title.addClassName('dormant_title');
    },
    rowChosen: function(c) {
        if(c.url) {
            new Ajax.Request(c.url, {
                method:'get',
                onloading: function(ev) {
                    c.content.update('Loading');
                },
                onSuccess: function(resp) {
                    c.content.update(resp.responseText);   
                    Effect.BlindDown(c.content, {'duration':1});
                },
                onFailure: function(ev) {
                    c.content.update('Error');
                }
            });
        }
    }
}
