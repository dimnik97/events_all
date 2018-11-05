// ------------------------------------------------------------------------------------------------------------------
    /**
     * Кастомный мультиселект
     *
     */
    $('.custom_multiply_select_items').on('click', '.multiply_select_item', function () {
        if ($('.remove_categories').length < 3) {
            $('.custom_multiply_select').append('<span class="remove_categories" data-categories_id="' +
                $(this).data('categories_id') + '" data-categories_description="'+ $(this).data('categories_description') +'">'+ $(this).html() + ' </span>');
            $(this).remove();

            // Добавить проверку на редактирование
            var categories = [];
            $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
                var $selector = $('.column_'+ (key + 1), '.recommend_image_block'), this_category;

                if ($selector.attr('category_name') !== $(this).data('categories_description')) {
                    var is_new = true;
                    $selector.attr('category_name', $(this).data('categories_description'));
                    $selector.css('display', 'block');
                }

                let category = $(this).data('categories_description');
                if (category && category !== '') {
                    categories += category + ',';
                    this_category = category;
                }
                if (is_new) {
                    $.ajax({
                        type: "POST",
                        url: '/events/get_images_by_categories',
                        data: {
                            'categories': this_category
                        },
                        dataType: 'json',
                        success: function(data) {
                            $selector.show();
                            $('.category_name_column_'+ (key + 1), '.recommend_image_block').html(category);
                            for (let i = 0; i < data.length; i ++) {
                                $selector.append('<div class="rec_im"><img src="/' + data[i] + '"></div>');
                            }
                        }
                    });
                }
            });
            let category_array = categories.split(',');

            set_default_image_to_event(category_array)
        }
    });

    /**
     * Динамическая подгрузка дефолтных картинок для событий
     *
     */
    $('.custom_multiply_select').on('click', '.remove_categories', function () {
        $('.custom_multiply_select_items').append('<span class="multiply_select_item" data-categories_id="'+
            $(this).data('categories_id') + '" data-categories_description="'+ $(this).data('categories_description') +'">'+ $(this).html()+'</span>');
        $(this).remove();

        // Добавить проверку на редактирование
        let categories = [];
        $('.custom_multiply_select').find('.remove_categories').each(function (key, value) {
            let $selector = $('.column_'+ (key + 1), '.recommend_image_block'), this_category;
            if ($selector.attr('category_name') !== $(this).data('categories_description')) {
                var is_new = true;
            }

            let category = $(this).data('categories_description');
            if (category && category !== '') {
                categories += category + ',';
                this_category = category;
            }
            if (is_new) {
                let x = $('[category_name = ' + this_category + ']').html();
                $('.column_'+ (key + 1), '.recommend_image_block').html(x);
                $selector.attr('category_name', $(this).data('categories_description'));
            }
        });

        if (categories.length === 0) {
            $('.recommend_img', '.recommend_image_block').each(function () {
                $(this).attr('category_name', '');
                $(this).attr('image_name', '');
                $(this).css('display', 'none');
                $(this).find('.rec_im').remove();
            });
            $('.event_avatar').attr('src', '/media/avatar_event_default/default.png');
            return
        } else {
            let category_array = categories.split(','), flag, i = 1, j = 0, category_array_ = category_array.slice();

            for (i; i < 4; i++) {  // Нумерация с единицы
                flag = false;
                let $selector = $('.column_' + i, '.recommend_image_block');
                for (j = 0; j < category_array.length; j++) {
                    if ($selector.attr('category_name') === category_array[j]) {
                        delete category_array[j];
                        flag = true;
                    }
                }
                if (flag === false) {
                    $selector.attr('category_name', '');
                    $selector.attr('image_name', '');
                    $selector.css('display', 'none');
                    $selector.find('.rec_im').remove();
                }
            }

            set_default_image_to_event(category_array_)
        }
    });

    // ------------------------------------------------------------------------------------------------------------------