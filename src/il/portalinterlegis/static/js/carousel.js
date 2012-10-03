$(function() {
    $("div.carousel")
        .carousel({pagination: true,
                   loop: true,
                   nextBtn: '',
                   prevBtn: '',
                   autoSlide: true,
                   autoSlideInterval: 8000});
    function next_previous_buttons(elts) {
        return elts.carousel.parent().children('.next-previous-buttons');
    };
    $("div.products-services")
        .carousel({pagination: false,
                   nextBtnInsertFn: function (elts) {
                       return next_previous_buttons(elts).children('input[value="Next"]');
                   },
                   prevBtnInsertFn: function (elts) {
                       return next_previous_buttons(elts).children('input[value="Previous"]');
                   },
                   loop: true});
});
