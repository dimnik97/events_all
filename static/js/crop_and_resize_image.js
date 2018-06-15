$('body').on('change', '#id_load_image', function (e) {
    var file = document.getElementById("id_load_image").files[0];
    $('.to_second_step').on('click', function () {
        to_second_step();
    });

    $('span.rotate-right').on('click', function () {
        rotate_image('right');
    });

    $('span.rotate-left').on('click', function () {
        rotate_image('left');
    });

    if (file.size < 26214400) {
        var $image = $('#id_image');
        $image.hide();
        $image.css('cursor', 'default');

        var form = new FormData($('.uploader').find('form').get(0));
        $('.upload-progress').show();
        $.ajax({
            url: url,
            type: 'POST',
            data: form,
            async: true,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            success: function (response) {
                $('.upload-progress').hide();
                if (response.status == 200) {
                    var coefficient = parseFloat(response.image_info.coefficient),
                        $image_ = $('#output_image'),
                        max_width = '500px',
                        max_height = '500px';

                    orig_height = response.image_info.height;
                    orig_width = response.image_info.width;
                    if (coefficient < 1) {
                        $image_.css('width', 'auto').css('height', max_height);
                    } else if (coefficient == 1){
                        $image_.css('width', max_width).css('height', max_height);
                    } else if (coefficient > 1) {
                        $image_.css('width', max_width).css('height', 'auto');
                    }
                    $image_.hide();
                    $image_.attr('src',response.link);

                    var img = new Image();
                    img.onload = function () {
                        var $image_ = $('#output_image'),
                            $help_image_div = $('.help_image_div');
                        var middle_height = ($('.uploader').outerHeight() - $image_.outerHeight(true)) / 2,
                            middle_width = ($('.uploader').outerWidth() - $image_.outerWidth(true)) / 2;
                        $image_.css('margin-top', String(middle_height) + 'px').css('margin-left', String(middle_width) + 'px');
                        $help_image_div.css('margin-top', String(middle_height) + 'px').
                        css('margin-left', String(middle_width) + 'px').
                        css('height', $image_.height() + 'px').
                        css('width', $image_.width() + 'px');
                        $help_image_div.css('z-index', 2);
                        $image_.show();
                        imgAreaSelect_($help_image_div, '');
                        $reset_.show();
                    };
                    img.src = response.link;
                    $('.rotate_buttons').show();
                } else if (response.status == 'size_error') {
                    text.text('Размер загружаемого файла не должен превышать 25МБ')
                }
                else {
                    // try {
                    //     var error = JSON.parse(response.error);
                    //     alert('Vailed to upload! ' + error['data']['error'] + ', error_code: ' + error['status']);
                    // }catch(error){
                    //     alert('Vailed to upload! ' + response.error + ', error_code :' + response.status);
                    // }
                    console.log(response);
                }
            },
            error: function(response) {
                console.log("error", response);
                $('.upload-progress').hide();
            }
        });
    }
    else {
        $('#file_info').text('Размер файла превышает 25МБ!')
    }
});

function rotate_image(direction) {
    var $div_image_ = $('#div_output_image'),
        angle = $div_image_.getRotateAngle();

    if (direction == 'left') {
        angle = parseInt(angle) + 270;
        if (angle > 360)
            angle = 360 - angle;
    }
    else
        angle = parseInt(angle) + 90;
    if (angle == 360)
        angle = 0;

    $div_image_.rotate(angle);
    var $help_image_div = $('.help_image_div'),
        width = $help_image_div.width(),
        height = $help_image_div.height(),
        margin_top = $help_image_div.css('margin-top'),
        margin_left = $help_image_div.css('margin-left');

    $help_image_div
        .data('rotate', angle)
        .width(height)
        .height(width)
        .css('margin-top', margin_left)
        .css('margin-left', margin_top);

    $help_image_div.imgAreaSelect({
        remove: true
    });
    imgAreaSelect_($help_image_div, '');
}

var crop_x1,
    crop_x2,
    crop_y1,
    crop_y2,
    crop_height,
    crop_width;

function imgAreaSelect_($help_image_div, aspectRatio='') {
    var ias = $help_image_div.imgAreaSelect({
        handles: true,
        instance: true,
        aspectRatio: aspectRatio,
        minWidth: '100',
        minHeight: '100',
        persistent: true,
        // parent: $('.imgareaselect_wrapper'),
        onSelectEnd: function (img, selection) {
            crop_x1 = selection.x1;
            crop_x2 = selection.x2;
            crop_y1 = selection.y1;
            crop_y2 = selection.y2;
            crop_height = selection.height;
            crop_width = selection.width;
        }
    });
    var x1 = $help_image_div.width() / 2 - 100,
        y1 = $help_image_div.height() / 2 - 100,
        x2 = $help_image_div.width() / 2 + 100,
        y2 = $help_image_div.height() / 2 + 100;
    ias.setSelection(x1, y1, x2, y2, true);
    ias.setOptions({ show: true });
    ias.update();
    var selection = ias.getSelection();
    crop_x1 = selection.x1;
    crop_x2 = selection.x2;
    crop_y1 = selection.y1;
    crop_y2 = selection.y2;
    crop_height = selection.height;
    crop_width = selection.width;
}

$('#uploader').on('dragenter', function () {
    e.stopPropagation();
    e.preventDefault();
})
$('#uploader').on('dragover', function () {
    e.stopPropagation();
    e.preventDefault();
})
$('#uploader').on('drop', function () {
    e.stopPropagation();
    e.preventDefault();
    var dt = e.dataTransfer;
    var files = dt.files;

    imageLoader.files = files;
});


function reset_all() {
    var $uploader = $('.uploader'),
        $input_field = $('#id_image', $uploader),
        $img = $('#output_image', $uploader),
        $help_image_div = $('.help_image_div', $uploader),
        $div_output_image = $('#div_output_image', $uploader);

    $div_output_image.rotate(0);
    $help_image_div.imgAreaSelect({
        remove: true
    });
    $input_field.val();
    $img.remove();
    $input_field.show();
    $help_image_div.remove();
    $div_output_image.append('<img id="output_image"/>');
    $uploader.append('<div class="help_image_div"></div>');
    $('.help_image_div').css('z-index', 0);
    $reset_.hide();
}

function to_second_step() {
    var $help_image_div = $('.help_image_div'),
        form = new FormData($('.uploader').find('form').get(0));

    var crop_y = orig_height / $help_image_div.height(),
        crop_x = orig_width / $help_image_div.width();
    var crop_x1_ = crop_x1 * crop_x,
        crop_x2_ = crop_x2 * crop_x,
        crop_y1_ = crop_y1 * crop_y,
        crop_y2_ = crop_y2 * crop_y,
        crop_height_ = crop_height * crop_y,
        crop_width_ = crop_width * crop_x;

    form.append('crop_x1', crop_x1_);
    form.append('crop_x2', crop_x2_);
    form.append('crop_y1', crop_y1_);
    form.append('crop_y2', crop_y2_);
    form.append('crop_height', crop_height_);
    form.append('crop_width', crop_width_);
    form.append('rotate', $help_image_div.data('rotate'));
    $.ajax({
        url: save_url,
        type: 'POST',
        data: form,
        async: true,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        success: function (response) {
            $('.upload-progress').show();
            var text = $('#file_info');
            if (response.status == 200) {
                text.text('Успешно сохранено');
            } else if (response.status == 'size_error') {
                text.text('Размер загружаемого файла не должен превышать 25МБ')
            }
            else {
                console.log(response);
            }
        },
        error: function(response) {
            console.log("error", response);
            $('.upload-progress').hide();
        }
    });
};


function load_reduced_image() {
    imgAreaSelect_($('#output_image'), '1:1', $('.uploader_mini'));
    $('.change_mini').off('click').on('click',function () {
        var save_url = $('.CropImageModule_wrapper_mini').data('save_url'),
            img = $('#output_image'),
            orig_height = $('#div_output_image_mini').data('orig_height'),
            orig_width = $('#div_output_image_mini').data('orig_width'),
            crop_y = orig_height / img.height(),
            crop_x = orig_width / img.width(),
            form = {
                'crop_x1': crop_x1 * crop_x,
                'crop_x2': crop_x2 * crop_x,
                'crop_y1': crop_y1 * crop_y,
                'crop_y2': crop_y2 * crop_y,
                'image_type': 'mini',
            };
        $.ajax({
            url: save_url,
            type: 'POST',
            data: form,
            success: function (response) {
                $('.upload-progress').hide();
                if (response.status == 200) {
                    console.log('OK')
                } else if (response.status == 'size_error') {
                    text.text('Размер загружаемого файла не должен превышать 25МБ')
                }
                else {
                    console.log(response);
                }
            },
            error: function(response) {
                console.log("error", response);
                $('.upload-progress').hide();
            }
        });
    })

}





