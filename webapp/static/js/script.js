$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

// 
$(document).ready(function () {
    $('#btn_ajax').click(function () {
        alert('Hello World');
        
    });
});
$(document).ready(function () {
    $('input[type=number]').on('keydown', function (e) {
        if (e.which == 189 || e.which == 109 || e.which == 173) {
            e.preventDefault();
        };
        if ($(this).val() < 0) {
            $(this).val(0);
        };
    });
    $('input[type=number]').on('click', function (e) {
        if ($(this).val() < 0) {
            $(this).val(0);
        };
    });
   
});
