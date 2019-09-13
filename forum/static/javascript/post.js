$(document).ready(function () {

    var curr_grade = "";
    var curr_placement = "";
    var title_select = $('[name=grade-input]');
    var placement_select = $('[name=placement]');
    var json_data;

    title_select.change(function () {
        curr_grade = $(this).val();
        if (curr_placement !== "") {
            query_classes()
        }

    });

    placement_select.change(function () {
        curr_placement = $("option:selected", this).text();
        if (curr_grade !== "") {
            query_classes()
        }
    });

    function query_classes() {
        var get_data = {
            grade: curr_grade,
            placement: curr_placement,
        };

        $.get(class_query_url, get_data, function (data) {
            json_data = data;
            update_dropdown()
        });
    }

    var toType = function (obj) {
        return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
    };

    var class_select = $('#subject-field');

    function update_dropdown() {
        var length = Object.keys(json_data).length;

        class_select.empty().append(
            $('<option></option>').val("").html("-- Topics/Classes --").attr('disabled', 'disabled').attr('selected', 'selected'),
            $('<option></option>').val("general").html("General"),
        );

        for (var i = 0; i < length; i++) {
            var class_pk = json_data[i]["pk"];
            var class_name = json_data[i]["fields"]["class_name"];
            class_select.append(
                $('<option></option>').val(class_pk).html(class_name),
            )
        }

    }
});
