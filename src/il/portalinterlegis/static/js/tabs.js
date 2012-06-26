$(function() {
    $(".il-tabs > ul").tabs(".il-tabs > div");

    // TODO: refactor this to go with the way of JQuery Tools
    // from http://css-tricks.com/tabs-with-round-out-borders/
	$(".il-tabs > ul > li").click(function(e) {
		e.preventDefault();
		$("li").removeClass("active");
		$(this).addClass("active");
	});
    // synchronize start "li.active" (for css) with "a.current"
    $(".il-tabs > ul > li > a.current").parent().addClass('active')
});
