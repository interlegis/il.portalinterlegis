$(function() {
    $("div.carousel")
        .carousel({pagination: true,
                   loop: true,
                   nextBtn: '',
                   prevBtn: '',
                   autoSlide: true,
                   autoSlideInterval: 5000});
    $("div.carousel-products")
        .carousel({pagination: false,
                   nextBtn: '',
                   prevBtn: '',
                   loop: true});
});
