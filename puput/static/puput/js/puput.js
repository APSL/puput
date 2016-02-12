$(document).ready(function () {
    //Menu > Sidebar
    $('.menu .parent:not(".active") a').next('.sub').css('display', 'none');
    $('.menu .parent a .open-sub').click(function (event) {
        event.preventDefault();

        if ($(this).closest('.parent').hasClass('active')) {
            $(this).parent().next('.sub').slideUp(300);
            $(this).closest('.parent').removeClass('active');
        } else {
            $(this).parent().next('.sub').slideDown(300);
            $(this).closest('.parent').addClass('active');
        }
    });
});
