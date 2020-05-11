odoo.define('event_stage_color.calendar_model', function (require){
"use strict";

var calendarModel = require('web.CalendarModel');
var rpc = require('web.rpc');

calendarModel.include({
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.stages = rpc.query({model: 'calendar.event.stage', method: 'search_read', args: [[]],fields: ['id','color']}).then(function (result) {
                return result
            });
        },


        _loadColors: function (element, events) {
            var fieldName = this.fieldColor;
             _.each(events, function (event) {
                 _.each(this.stages, function (stage) {
                     if(event.record[fieldName][0] === stage['id']){
                         event.color_index = stage['color']
                     }
                 });
            });
            this.model_color = this.fields[fieldName].relation || element.model;
        },

        _loadRecordsToFilters: function (element, events) {
            var self = this;
            var new_filters = {};
            var to_read = {};

            _.each(this.data.filters, function (filter, fieldName) {
                var field = self.fields[fieldName];

                new_filters[fieldName] = filter;
                if (filter.write_model) {
                    if (field.relation === self.model_color) {
                        _.each(filter.filters, function (f) {
                            f.color_index = f.value;
                        });
                    }
                    return;
                }

                _.each(filter.filters, function (filter) {
                    filter.display = !filter.active;
                });

                var fs = [];
                var undefined_fs = [];
                _.each(events, function (event) {
                    var data =  event.record[fieldName];
                    if (!_.contains(['many2many', 'one2many'], field.type)) {
                        data = [data];
                    } else {
                        to_read[field.relation] = (to_read[field.relation] || []).concat(data);
                    }
                    _.each(data, function (_value) {
                        var value = _.isArray(_value) ? _value[0] : _value;
                        var f = {
                            'color_index': self.model_color === (field.relation || element.model) ? value : false,
                            'value': value,
                            'label': fieldUtils.format[field.type](_value, field) || _t("Undefined"),
                            'avatar_model': field.relation || element.model,
                        };
                        // if field used as color does not have value then push filter in undefined_fs,
                        // such filters should come last in filter list with Undefined string, later merge it with fs
                        value ? fs.push(f) : undefined_fs.push(f);
                    });
                });
                _.each(_.union(fs, undefined_fs), function (f) {
                    var f1 = _.findWhere(filter.filters, f);
                    if (f1) {
                        f1.display = true;
                    } else {
                        f.display = f.active = true;
                        filter.filters.push(f);
                    }
                });
            });

            var defs = [];
            _.each(to_read, function (ids, model) {
                defs.push(self._rpc({
                        model: model,
                        method: 'name_get',
                        args: [_.uniq(ids)],
                    })
                    .then(function (res) {
                        to_read[model] = _.object(res);
                    }));
            });
            return $.when.apply($, defs).then(function () {
                _.each(self.data.filters, function (filter) {
                    if (filter.write_model) {
                        return;
                    }
                    if (filter.filters.length && (filter.filters[0].avatar_model in to_read)) {
                        _.each(filter.filters, function (f) {
                            f.label = to_read[f.avatar_model][f.value];
                        });
                    }
                });
            });
        },
    });
});