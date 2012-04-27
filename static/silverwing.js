$(function(){

    var Element = Backbone.Model.extend({
        default: {
            name: '',
            pyclass: '',
            attributes: []
        }
    });

    var ElementCollection = Backbone.Collection.extend({
        model: Element
    });

    var ElementEditView = Backbone.View.extend({
        tagName: 'fieldset',
        events: {
            'click .btn-add-attr': 'addAttr',
            'click .btn-remove-attr': 'removeAttr'
        },
        render: function() {
            this.$el.html(this.model.name);
            return this;
        },
        addAttr: function() {
            this.model.attributes.push({});
        },
        removeAttr: function() {
        }
    });

});