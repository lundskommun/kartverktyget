/// <reference path="../typings/jquery/jquery.d.ts" />
/// <reference path="../typings/local-js-cookie.d.ts" />

$('#guide-carousel').carousel({
    interval: false,
});

$('#guide-prev').click(function(event) {
    $('#guide-carousel').carousel('prev');
});

$('#guide-next').click(function(event) {
    $('#guide-carousel').carousel('next');
});

$(document).ready(function() {
    var has_visited = Cookies.get('has-visited');

    if (!(has_visited === 'y')) {
        $('#guide-box').modal();
    }

    Cookies.set('has-visited', 'y');
})
