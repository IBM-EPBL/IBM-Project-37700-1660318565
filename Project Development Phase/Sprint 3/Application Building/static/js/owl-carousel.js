$(document).ready(function(){
    $("#testimonial-slider").owlCarousel({
        items:2,
        itemsDesktop:[800,2],
        itemsDesktopSmall:[789,2],
        itemsTablet:[768,2],
        itemsMobile:[650,1],
        pagination:false,
        navigation:true,
        navigationText:["",""],
        autoPlay:true
    });
});

AOS.init();

