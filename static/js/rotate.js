var $id_image = $('#id_image'),
    $reset_ = $('.reset_'),
    $to_first_step = $('.to_first_step');

    $id_image.attr('accept', 'image/*');
    $reset_.hide();
    $to_first_step.hide();

$('#id_image').on('change', function (e) {
    var file = document.getElementById("id_image").files[0],
        ext = "не определилось",
        text = $('#file_info');

    if (file.size < 26214400) {
        text.text([
            "Размер файла: " + file.size + " B",
            "Расширение: " + ext,
            "MIME тип: " + file.type
        ].join("<br>"));

        var $image = $('#id_image');
        $image.hide();
        $image.css('cursor', 'default');

        var form = new FormData($('.uploader').find('form').get(0));
        $('.upload-progress').show();
        $.ajax({
            url: '/profile/load_image',
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
                        imgAreaSelect_($help_image_div);
                        $reset_.show();
                    }
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

$('span.rotate-right').on('click', function () {
    rotate_image('right');
});

$('span.rotate-left').on('click', function () {
    rotate_image('left');
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
        .width(height)
        .height(width)
        .css('margin-top', margin_left)
        .css('margin-left', margin_top);

    $help_image_div.imgAreaSelect({
        remove: true
    });
    imgAreaSelect_($help_image_div);
}

var crop_x1,
    crop_x2,
    crop_y1,
    crop_y2,
    crop_height,
    crop_width;

function imgAreaSelect_($help_image_div) {
    var ias = $help_image_div.imgAreaSelect({
        handles: true,
        instance: true,
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

    //this code line fires your 'handleImage' function (imageLoader change event)
    imageLoader.files = files;
});


function reset_all() {
    var $uploader = $('.uploader'),
        $input_field = $('#id_image', $uploader),
        $img = $('#output_image', $uploader),
        $help_image_div = $('.help_image_div', $uploader),
        $div_output_image = $('#div_output_image', $uploader);

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

$('.to_second_step').on('click', function () {
    var src = $('#output_image').attr('src'),
        $help_image_div = $('.help_image_div');

    $help_image_div.getSelection();
    $.ajax({
            url: '/profile/load_image_to_crop',
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
});




