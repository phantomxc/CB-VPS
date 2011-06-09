
Tabs = Class.create();

    Tabs.prototype = {
    
    initialize: function(baseElement) {
        this.baseElement = $(baseElement);
        this.ul = new Element('ul');
        this.baseElement.update(this.ul);
        this.loadingdiv = null;
        this.chosen = null;
        this.ajaxGoing = false;
        this.globalParams = {};
    },
        
    addTab: function(title, div, url, params, func) {
        var li = new Element('li').insert(title);
        li.title = title;
        li.content = $(div);
        li.content.hide();
        li.addClassName('dormant');
        li.url = url;
        li.params = params || function() {return{}};
        li.processor = func || null;
        li.observe('click', function(ev) {
            this.chooseTab(li);
        }.bind(this));
        
        this.ul.insert(li);
        return li;
    },
    removeTab: function(li) {
        li.content.hide();
        li.remove();
    },

    start: function(li) {
        this.chooseTab(li);
    },
    
    chooseTab: function(li) {
        if (this.ajaxGoing) {
            return false;
        }
        if (this.chosen && this.chosen != li) {
            this.chosen.content.hide();
            this.chosen.removeClassName('active');
            this.chosen.addClassName('dormant');
        }
        this.chosen = li;
        li.content.hide();
        li.removeClassName('dormant');
        li.addClassName('active');
       
        if (li.url) {
            new Ajax.Request(li.url, {
                method: 'POST',
                parameters: li.params(),
                
                onSuccess: function(li, r) {
                    this.showError('');
                    li.content.update(r.responseText);
                    if (li.processor) {
                        li.processor(li);
                    }
                    li.content.show();
                }.bind(this, li),
                
                onFailure: function(li, r) {
                    if (this.loadingdiv) {
                        this.loadingdiv.hide();
                    }
                    this.showError('error');
                    li.content.show();
                }.bind(this, li),
            
                onComplete: function(r) {
                    if (this.loadingdiv) {
                        this.loadingdiv.hide();
                    }
                    this.ajaxGoing = false;
                }.bind(this)
            });
            
            this.ajaxGoing = true;
            if (this.loadingdiv) {
                this.loadingdiv.show();
            }
        } else {
            if (this.loadingdiv) {
                this.loadingdiv.hide();
            }
            li.content.show();
            if (li.processor) {
                li.processor();
            }
        }
    },
    showError: function() {
    }
}
