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
                   loop: true});
});
