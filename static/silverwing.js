
//
// Models
//

var Attribute = Backbone.Model.extend({
    defaults: {
        name: '',
        defaultVal: '',
        'type': 'value'
    },
    initialize: function() {
        if(!this.get('defaultVal')) {
            this.set('defaultVal', this.defaults.defaultVal);
        }
    }
});

var AttributeList = Backbone.Collection.extend({
    model: Attribute,
    url: '/attributes'
});

var Element = Backbone.Model.extend({
    defaults: {
        name: 'New Element',
        pyclass: '',
        attributes: new AttributeList(),
        'checked': false
    },
    initialize: function(data) {
        data = _.defaults(data || {}, this.defaults);
        if(data['attributes'] && _.isArray(data['attributes'])) {
            this.set('attributes', new AttributeList(data['attributes']));
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

var AttributeEditRowView = Backbone.View.extend({
    model: Attribute,
    tagName: 'tr',
    events: {
        'change .a-update': 'updateModel',
        'click .btn-remove-attr': 'removeAttr'
    },
    render: function() {
        var isValue = this.model.get('type') == 'value';
        var isText = this.model.get('type') == 'text';
        var prefix = 'attrs.' + this.model.cid + '.';
        this.$el.html('' +
            '<td><input type="text" name="' + prefix + 'name" class="a-name a-update" value="' + this.model.get('name') + '" /></td>' +
            '<td>' +
            '  <select name="' + prefix + 'type" class="a-type a-update">' +
            '    <option value="value" ' + (isValue ? 'selected="selected"' : '') + '>Value (100 char limit)</option>' +
            '    <option value="text" ' + (isText ? 'selected="selected"' : '') + '>Text</option>' +
            '  </select>' +
            '</td>' +
            '<td>' +
            '  <div class="attr-default ' + this.model.cid + '">' +
            '    <textarea name="' + prefix + 'default" class="a-default a-update">' + this.model.get('defaultVal') + '</textarea></div>' +
            '</td>' +
            '<td>' +
            '  <a href="" class="btn-remove-attr"><i class="icon-minus-sign"></i></a>' +
            '</td>');
        return this;
    },
    updateModel: function(e) {
        this.model.set({
            name: this.$('.a-name').val(),
            type: this.$('.a-type').val(),
            defaultVal: this.$('.a-default').val()
        });
    },
    removeAttr: function(e) {
        e.preventDefault();
        this.model.destroy();
    }
});
    
var AttributeListEditView = Backbone.View.extend({
    model: AttributeList,
    render: function() {
        self = this;
        this.$el.html('');
        this.model.each(function(attr) {
            self.$el.append((new AttributeEditRowView({model: attr})).render().el);
        });
        return this;
    }
});

var ElementEditView = Backbone.View.extend({
    model: Element,
    events: {
        'click .btn-add-attr': 'addAttr',
        'change .e-name': 'updateName'
    },
    initialize: function() {
        this.formLegend = this.$('.form-legend');
        this.elementName = this.$('.e-name');
        this.elementClass = this.$('.e-class');
        this.attrsTbody = this.options.attributesEl.children('tbody');

        this.model.bind('change', this.render, this);
        this.model.get('attributes').bind('add', this.render, this);
        this.model.get('attributes').bind('remove', this.render, this);
        
        this.render();
    },
    render: function() {
        this.formLegend.html(this.model.escape('name'));
        this.elementName.val(this.model.get('name'));
        this.elementClass.val(this.model.get('pyclass'));
        
        new AttributeListEditView({
            el: this.attrsTbody,
            model: this.model.get('attributes')
        }).render();
        
        if(this.model.get('attributes').length == 0) {
            this.options.attributesEl.hide();
        } else {
            this.options.attributesEl.show();
        }
        
        return this;
    },
    updateName: function(e) {
        this.model.set('name', $(e.target).val());
    },
    addAttr: function(e) {
        e.preventDefault();
        this.model.get('attributes').add(new Attribute());
    }
});

var ElementRowView = Backbone.View.extend({
    model: Element,
    tagName: 'tr',
    events: {
        'change .e-update': 'updateModel'
    },
    render: function() {
        var attrNames = this.model.get('attributes').models.map(function(attr) {
            return attr.get('name');
        });
        this.$el.html('' +
            '<td><a href="/elements/' + this.model.get('id') + '">' + this.model.get('name') + '</a></td>' +
            '<td>' + this.model.get('pyclass') + '</td>' +
            '<td>' + attrNames.join(', ') + '</td>' +
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
    events: {
        'click .btnDelete': 'deleteElements'
    },
    initialize: function() {
        this.btnDelete = this.$el.children('.btnDelete');
        this.elements = this.options.elements || new ElementList();
    },
    render: function() {
        if(this.elements.length > 0) {
            this.btnDelete.removeClass('disabled');
        } else {
            this.btnDelete.addClass('disabled');
        }
        return this;
    },
    deleteElements: function(e) {
        e.preventDefault();
        this.elements.each(function(elem) {
            elem.destroy();
        });
    }
});

var ElementListView = Backbone.View.extend({
    model: ElementList,
    initialize: function() {
        this.elemsTbody = this.options.elemsTblEl.children('tbody');
        this.model.bind('change', this.renderToolbar, this);
        this.model.bind('destroy', this.render, this);
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
        this.renderToolbar();
        return this;
    },
    renderToolbar: function() {
        var checkedElems = this.model.filter(function(elem) {
            return elem.get('checked');
        });
        new ElementListToolbarView({
            el: this.options.toolbarEl,
            elements: new ElementList(checkedElems)
        }).render();
    }
});
















