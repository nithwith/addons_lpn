odoo.define('event_stage_color.calendar_model', function (require){
"use strict";

    var CalendarRenderer = require('web.CalendarRenderer');
    var CalendarModel = require('web.CalendarModel');

    CalendarRenderer.include({
        init: function (parent, state, params) {
            // Fullfil the filter widget
            this._super.apply(this, arguments);
            //TODO simplify for
            for (const [key, data] of Object.entries(this.state.data)) {
                var id = data.record.stage_id[0]
                var color = data.record.stage_color
                this.color_map[id] = color
            }
        },
    });

    CalendarModel.include({
        _recordToCalendarEvent: function (evt) {
            // Fullfil the event color
            var result = this._super.apply(this, arguments);
            result['color'] = evt.stage_color;
            return result;
        },
    });
});