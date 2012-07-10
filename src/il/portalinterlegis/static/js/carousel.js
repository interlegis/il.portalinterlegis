$(function() {
    $("div.carousel")
        .carousel({pagination: true,
                   loop: true,
                   nextBtn: '',
                   prevBtn: '',
                   autoSlide: true,
                   autoSlideInterval: 5000});
    $("div.products-services")
        .carousel({pagination: false,
                   nextBtnInsertFn: function (elts) {
                       var buttons = elts.carousel.parent().parent().children('.next-previous-buttons');
                       return buttons.children('input[value="Next"]')
                   },
                   prevBtnInsertFn: function (elts) {
                       var buttons = elts.carousel.parent().parent().children('.next-previous-buttons');
                       return buttons.children('input[value="Previous"]')
                   },
                   loop: true});
});
