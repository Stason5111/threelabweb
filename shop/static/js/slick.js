$('.autoplay').slick({
  slidesToShow: 4,
  slidesToScroll: 1,
  variableWidth: true,
  autoplay: true,
  autoplaySpeed: 1000,
  lazyLoad: 'ondemand',
  prevArrow: $('.slick-autoplay-prev'),
  nextArrow: $('.slick-autoplay-next'),
});

$('.multiple-items').slick({
  infinite: true,
  slidesToShow: 4,
  slidesToScroll: 1,
  variableWidth: true,
  lazyLoad: 'ondemand',
  prevArrow: $('.slick-multiple-prev'),
  nextArrow: $('.slick-multiple-next'),
});