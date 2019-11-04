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


});
