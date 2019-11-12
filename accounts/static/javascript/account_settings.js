//https://www.w3schools.com/howto/howto_js_filter_dropdown.asp
$(document).ready(function () {
    var add_class = $("#add-class");
    var input = $("input");

    add_class.click(function () {
        searchFunction()
    });
    input.keyup(function () {
        filterFunction()
    });

    /* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
    function searchFunction() {
        $(".dropdown-content").toggle();
    }

    function filterFunction() {
        var input, filter, ul, li, a, i;
        input = $(".class-search");
        filter = input.val().toUpperCase();
        div = $("#classDropdown");
        a = $("#classDropdown").children("a");
        jQuery.each(a, function (index, item) {
            txtValue = $(item).text();
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                $(item).css({"display": ""});

            } else {
                $(item).css({"display": "none"});
            }
        })

    }


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    //Deals with adding the school classes from search bar
    var search_school_class = $(".class-item");
    var remove_btn = $('.remove-class');

    search_school_class.click(function () {
        console.log('clicked');
        var id = Number($(this).attr('data-id'));
        var post_data = {
            class_id: id,
            action: "add"
        };

        send_to_server(post_data, FormSuccess, FormError);
        var div = remove_btn.parentsUntil("add-class-section-2");
        $(".add-class-section-2").append("<div class=\"class-name-div\" data-id=\"{{ class.id }}\"><h4 class=\"class-name-header\" data-id=\"" + id + "\">" + $(this).text() + "</h4> <a href=\"#\" class=\"remove-class w-button\"> <strong class=\"minus-symbol\">-</strong></a></div>")

    });

    remove_btn.click(function () {
        console.log('clicked');
        var id = Number($(this).parent().attr('data-id'));
        console.log($(this).attr('data-id'));
        var post_data = {
            class_id: id,
            action: "remove"
        };
        console.log(post_data);

        send_to_server(post_data, FormSuccess, FormError);
        var div = remove_btn.parent("[data-id=" + id + "]");
        div.remove()
    });

    function send_to_server(post_data, success_func = '', error_func = '') {
        var $url = "/accounts/settings/change-classes";
        $.ajax({
            url: $url,
            type: "POST",
            data: post_data,
            success: success_func,
            error: error_func,
        });
    }


    function FormSuccess(data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR)
    }

    function FormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown)
    }
});
