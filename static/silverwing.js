
//
// Models
//

var Attribute = Backbone.Model.extend({
    defaults: {
        name: '',
        defaultValue: '',
        'type': 'value'
    },
    initialize: function() {
        if(!this.get('defaultValue')) {
            this.set('defaultValue', this.defaults.defaultValue);
        }
    }
});

var AttributeList = Backbone.Collection.extend({
    model: Attribute,
    url: '/attributes'
});

var Element = Backbone.Model.extend({
    defaults: function() {
        return {
            name: '',
            pyclass: '',
            attributes: new AttributeList(),
            elements: new ElementList(),
            'checked': false
        };
    },
    initialize: function(data) {
        data = _.defaults(data || {}, this.defaults);
        if(data['attributes'] && _.isArray(data['attributes'])) {
            this.set('attributes', new AttributeList(data['attributes']));
        }
        if(data['elements'] && _.isArray(data['elements'])) {
            this.set('elements', new ElementList(data['elements']));
        }
    }
});

var ElementList = Backbone.Collection.extend({
    model: Element,
    url: '/elements'
});


//
// Views
//

var ElementEditView_AttributeRowView = Backbone.View.extend({
    model: AttributeList,
    render: function() {
        var self = this;
        this.$el.html('');
        this.model.each(function(attr) {
            self.$el.append('<tr>' +
                '  <td>' + attr.get('name') + '</td>' +
                '  <td><textarea name="attrs.' + attr.get('name') + '">' + attr.get('defaultValue') + '</textarea></td>' +
                '</tr>');
        });
        return this;
    }
});

var ElementEditView_ElementItemRowView = Backbone.View.extend({
    model: Element,
    tagName: 'tr',
    events: {
        'click .btnDelete': 'deleteModel',
        'change .name, .pyclass': 'updateModel'
    },
    render: function() {
        var self = this;
        var htmloptions = this.options.allElements.map(function(elem) {
            return '<option value="' + elem.get('id') + '"' +
                (elem.get('id') == self.model.get('id') ? ' selected="selected"' : '') +
                '>' + elem.get('name') + '</option>';
        });
        this.$el.html('' +
                '<td><input type="text" name="elems.' + this.model.cid + '.name" class="name" value="' + this.model.get('name') + '" /></td>' +
                '<td>' +
                '  <select name="elems.' + this.model.cid + '.pyclass" class="pyclass">' + htmloptions + '</select>' +
                '</td>' +
                '<td style="text-align:center;">' +
                '  <a href="" class="btnDelete"><i class="icon-minus-sign"></i></a>' +
                '</td>');
        return this;
    },
    updateModel: function(e) {
        this.model.set({
            name: this.$('.name').val(),
            pyclass: this.$('.pyclass').val()
        });
    },
    deleteModel: function(e) {
        e.preventDefault();
        this.model.destroy();
    }
});
var ElementEditView_ElementRowView = Backbone.View.extend({
    model: ElementList,
    events: {
        'click .btnAddElem': 'addElem'
    },
    initialize: function() {
        this.model.bind('add', this.render, this);
        this.model.bind('destroy', this.render, this);
    },
    render: function() {
        var self = this;
        this.$el.html('');
        this.model.each(function(model) {
            var view = new ElementEditView_ElementItemRowView({
                model: model,
                allElements: self.options.allElements
            });
            self.$el.append(view.render().el);
        });
        this.$el.append('<tr><td colspan="3"><a href="" class="btn btnAddElem"><i class="icon-plus-sign"></i> Add Element</a></td></tr>');
        return this;
    },
    addElem: function(e) {
        e.preventDefault();
        this.model.add(new Element());
    }
});

var ElementEditView = Backbone.View.extend({
    model: Element,
    events: {
        'change #pyclass': 'render'
    },
    initialize: function() {
        this.attrsTbody = this.options.attributesEl.children('tbody');
        this.pyclass = this.$('#pyclass');
        this.render();
    },
    render: function() {
        var self = this;
        var selected = this.options.allClasses.where({pyclass: this.pyclass.val()});
        selected = selected[0];
        var view = new ElementEditView_AttributeRowView({
            el: this.attrsTbody,
            model: selected.get('pyclass') == this.model.get('pyclass') ? this.model.get('attributes') : selected.get('attributes')});
        view.render();
        if(selected.get('pyclass') == 'silverwing.elements.Group') {
            this.options.subElemsEl.show();
            var view = new ElementEditView_ElementRowView({
                el: this.options.subElemsEl.find('tbody'),
                model: this.model.get('elements'),
                allElements: this.options.allElements});
            view.render();
        } else {
            this.options.subElemsEl.find('tbody').html('');
            this.options.subElemsEl.hide();
        }
        return this;
    }
});

var ElementRowView = Backbone.View.extend({
    model: Element,
    tagName: 'tr',
    events: {
        'change .e-update': 'updateModel'
    },
    render: function() {
        this.$el.html('' +
            '<td><a href="/elements/' + this.model.get('id') + '">' + this.model.get('name') + '</a></td>' +
            '<td>' + this.model.get('pyclass') + '</td>' +
            '<td style="text-align:center;">' +
            '  <input type="checkbox" class="e-update e-checked" name="elems.' + this.model.get('id') + '" />' +
            '</td>');
        return this;
    },
    updateModel: function() {
        this.model.set('checked', this.$('.e-checked').attr('checked') == 'checked');
    }
});

var ElementListToolbarView = Backbone.View.extend({
    model: ElementList,
    events: {
        'click .btnDelete': 'deleteElements'
    },
    initialize: function() {
        this.btnDelete = this.$el.children('.btnDelete');
        this.model.bind('change', this.render, this);
    },
    render: function() {
        if(this.checkedElems().length > 0) {
            this.btnDelete.removeClass('disabled');
        } else {
            this.btnDelete.addClass('disabled');
        }
        return this;
    },
    deleteElements: function(e) {
        e.preventDefault();
        _.each(this.checkedElems(), function(elem) {
            elem.destroy();
        });
    },
    checkedElems: function() {
        return this.model.filter(function(elem) {
            return elem.get('checked');
        });
    }
});

var ElementListView = Backbone.View.extend({
    model: ElementList,
    initialize: function() {
        this.elemsTbody = this.options.elemsTblEl.children('tbody');
        this.model.bind('destroy', this.render, this);
        new ElementListToolbarView({
            el: this.options.toolbarEl,
            model: this.model
        });
        this.render();
    },
    render: function() {
        var self = this;
        this.elemsTbody.html('');
        this.model.each(function(elem) {
            self.elemsTbody.append((new ElementRowView({model: elem})).render().$el);
        });
        if(this.model.length == 0) {
            this.options.elemsTblEl.hide();
        } else {
            this.options.elemsTblEl.show();
        }
        return this;
    }
});
















