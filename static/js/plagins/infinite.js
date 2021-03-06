/*!
Waypoints Infinite Scroll Shortcut - 4.0.1
Copyright © 2011-2016 Caleb Troughton
Licensed under the MIT license.
https://github.com/imakewebthings/waypoints/blob/master/licenses.txt
*/
(function() {
    'use strict'

    var $ = window.jQuery
    var Waypoint = window.Waypoint

    /* http://imakewebthings.com/waypoints/shortcuts/infinite-scroll */
    function Infinite(options) {
        this.options = $.extend({}, Infinite.defaults, options)
        this.container = this.options.element
        if (this.options.container !== 'auto') {
            this.container = this.options.container
        }
        this.$container = $(this.container)
        this.$reverse = $(this.reverse)
        this.more_by_class = $(this.more_by_class)
        this.$more = $(this.options.more)

        if (this.$more.length) {
            this.setupHandler()
            this.waypoint = new Waypoint(this.options)
        }
    }

    /* Private */
    Infinite.prototype.setupHandler = function() {
        this.options.handler = $.proxy(function() {
            this.options.onBeforePageLoad()
            this.destroy()
            this.$container.addClass(this.options.loadingClass)
            if (this.options.post) {
                $.ajax({
                    type: "POST",
                    url: $(this.options.more).attr('href'),
                    data: this.options.filter,
                    success: $.proxy(function (data) {
                        var $data = $($.parseHTML(data));
                        var $newMore;
                        if (this.options.more_by_class) {
                            this.options.more = '.' + $(this.options.more).attr('class');
                            $newMore = $data.filter('.' + $(this.options.more).attr('class'))
                        }
                        else {
                            let $more = this.options.more;
                            $newMore = $data.filter($more);
                        }
                        var $items = $data.find(this.options.items);
                        if (!$items.length) {
                            $items = $data.filter(this.options.items);
                        }
                        if (this.options.reverse)
                            this.$container.prepend($items);
                        else {
                            this.$container.append($items);
                        }

                        this.$container.removeClass(this.options.loadingClass)

                        if (!$newMore.length) {
                            $newMore = $data.filter(this.options.more)
                        }
                        if ($newMore.length) {
                            this.$more.replaceWith($newMore);
                            this.$more = $newMore;
                            this.waypoint = new Waypoint(this.options)
                        }
                        else {
                            this.$more.remove()
                        }

                        this.options.onAfterPageLoad($items)
                    }, this),
                });
            } else {
                $.get($(this.options.more).attr('href'), $.proxy(function (data) {
                    var $data = $($.parseHTML(data));
                    var $newMore = $data.filter(this.options.more);

                    var $items = $data.find(this.options.items);
                    if (!$items.length) {
                        $items = $data.filter(this.options.items);
                    }
                    if (this.options.reverse)
                        this.$container.prepend($items);
                    else {
                        this.$container.append($items);
                    }

                    this.$container.removeClass(this.options.loadingClass)

                    if (!$newMore.length) {
                        $newMore = $data.filter(this.options.more)
                    }
                    if ($newMore.length) {
                        this.$more.replaceWith($newMore)
                        this.$more = $newMore
                        this.waypoint = new Waypoint(this.options)
                    }
                    else {
                        this.$more.remove()
                    }

                    this.options.onAfterPageLoad($items)
                }, this))
            }
        }, this)
    }

    /* Public */
    Infinite.prototype.destroy = function() {
        if (this.waypoint) {
            this.waypoint.destroy()
        }
    }

    Infinite.defaults = {
        container: 'auto',
        reverse: false,
        items: '.infinite-item',
        more: '.infinite-more-link',
        offset: 'bottom-in-view',
        loadingClass: 'infinite-loading',
        onBeforePageLoad: $.noop,
        onAfterPageLoad: $.noop,
        post: false, // Для пост запросов, чтобы не парится с урлами и так далее
        filter: {}, // Фильтр
        more_by_class: false
    }

    Waypoint.Infinite = Infinite
}())
;