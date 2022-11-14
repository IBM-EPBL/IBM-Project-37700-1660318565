$(document).ready(function(){
  $(window).scroll(function () {
    $('.navbar').toggleClass('scrolled',$(this).scrollTop()>50);
});
});

