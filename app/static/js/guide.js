$('.collapse').on('show.bs.collapse', function () {
    console.log($(this).siblings());
    $(this).siblings('.collapse-heading').addClass('active');
});

$('.collapse').on('hide.bs.collapse', function () {
    console.log($(this).siblings());
    $(this).siblings('.collapse-heading').removeClass('active');
});