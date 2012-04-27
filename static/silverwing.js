
var Attribute = Backbone.Model.extend({
    defaults: {
        name: '',
        defaultValue: '',
        defaultText: '',
        'type': 'value'
    },
    
    initialize: function() {
        if(!this.get('defaultValue')) {
            this.set('defaultValue', this.defaults.defaultValue);
        }
        if(!this.get('defaultText')) {
            this.set('defaultText', this.defaults.defaultText);
        }
    }
});

var AttributeCollection = Backbone.Collection.extend({
    model: Attribute,
    localStorage: new Store('silverwing-attrs')
});

var Element = Backbone.Model.extend({
    defaults: {
        name: 'New Element',
        pyclass: '',
        attributes: new AttributeCollection()
    },
    
    initialize: function(data) {
        this.set('attributes', new AttributeCollection(data['attributes']));
    }
});

var AttributeEditRowView = Backbone.View.extend({
    model: Attribute,
    tagName: 'tr',
    events: {
        'change .a-update': 'updateModel',
        'change .a-type': 'render',
        'click .btn-remove-attr': 'removeAttr'
    },
    
    render: function() {
        var isValue = this.model.get('type') == 'value';
        var isText = this.model.get('type') == 'text';
        var prefix = 'attrs.' + this.model.cid + '.';
        this.$el.html('' +
            '  <td><input type="text" name="' + prefix + 'name" class="a-name a-update" value="' + this.model.get('name') + '" /></td>' +
            '  <td>' +
            '    <select name="' + prefix + 'type" class="a-type a-update">' +
            '      <option value="value" ' + (isValue ? 'selected="selected"' : '') + '>Value (100 char limit)</option>' +
            '      <option value="text" ' + (isText ? 'selected="selected"' : '') + '>Text</option>' +
            '    </select>' +
            '  </td>' +
            '  <td>' +
            '    <div class="attr-value ' + this.model.cid + ' ' + (isText ? 'hide' : '') + '">' +
            '      <textarea name="' + prefix + 'defaultValue" class="a-defaultValue a-update">' + this.model.get('defaultValue') + '</textarea></div>' +
            '    <div class="attr-text ' + this.model.cid + ' ' + (isValue ? 'hide' : '') + '">' +
            '      <textarea name="' + prefix + 'defaultText" class="a-defaultText a-update">' + this.model.get('defaultText') + '</textarea></div>' +
            '  </td>' +
            '  <td>' +
            '    <a href="" class="btn-remove-attr"><i class="icon-minus-sign"></i></a>' +
            '  </td>');
        return this;
    },
    
    updateModel: function(e) {
        this.model.set({
            name: this.$('.a-name').val(),
            type: this.$('.a-type').val(),
            defaultValue: this.$('.a-defaultValue').val(),
            defaultText: this.$('.a-defaultText').val()
        });
    },
    
    removeAttr: function(e) {
        e.preventDefault();
        this.model.destroy();
    }
});
    
var AttributeCollectionEditView = Backbone.View.extend({
    model: AttributeCollection,
    
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

        this.model.bind('change', this.render, this);
        this.model.get('attributes').bind('add', this.render, this);
        this.model.get('attributes').bind('remove', this.render, this);
        
        this.render();
    },
    
    render: function() {
        this.formLegend.html(this.model.escape('name'));
        this.elementName.val(this.model.get('name'));
        this.elementClass.val(this.model.get('pyclass'));
        
        if(this.model.get('attributes').length == 0) {
            this.options.attributesEl.hide();
        } else {
            this.options.attributesEl.show();
            new AttributeCollectionEditView({
                el: this.options.attributesEl.children('tbody'),
                model: this.model.get('attributes')
            }).render();
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
