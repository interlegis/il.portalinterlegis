$(function() {

    // initiate tabs plugin
    $(".il-tabs > ul").tabs(".il-tabs > div > div");

    // synchronize pane with current tab
    var current_tab = $(".il-tabs > ul > li > a.current").parent().attr("class");
    $(".il-tabs > div").attr("class", current_tab);

    // synchronize "li.active" with "a.current"
    $(".il-tabs > ul > li > a.current").parent().addClass("active");

    // TODO: refactor this to go with the way of JQuery Tools
    // from http://css-tricks.com/tabs-with-round-out-borders/
    $(".il-tabs > ul > li").click(function(e) {
        e.preventDefault();
        $("li").removeClass("active");
        $(this).addClass("active");
        // synchronize tab pane with current tab's class
        $(".il-tabs > div").attr("class", $(this).attr("class"));
    });

});
