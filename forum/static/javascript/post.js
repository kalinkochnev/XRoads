$(document).ready(function () {

    var curr_grade = "";
    var curr_subject = "";
    var title_select = $('[name=grade_input]');
    var subject_select = $('[name=subject_input]');
    var json_data;

    title_select.change(function () {
        curr_grade = $(this).val();
        if (curr_subject !== "") {
            query_classes()
        }

    });

    subject_select.change(function () {
        curr_subject = $("option:selected", this).val();
        if (curr_grade !== "") {
            query_classes()
        }
    });

    function query_classes() {
        var get_data = {
            grade: curr_grade,
            subject: curr_subject,
        };

        $.get(class_query_url, get_data, function (data) {
            console.log(data);
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
        );

        for (var i = 0; i < length; i++) {
            var class_pk = json_data[i]["pk"];
            var name = json_data[i]["fields"]["name"];
            var placement = json_data[i]["fields"]["placement"];
            class_select.append(
                $('<option></option>').val(class_pk).html(name + " " + placement),
            )
        }

    }

});
