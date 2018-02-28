// (function() {
const setMenuToSearch = function () {
    $('.item.active').removeClass('active');
    $('#menu-search-field-item').addClass('active');
};

const search = function (e) {
    console.log('a');
    setMenuToSearch();
    $.ajax({
        url: '/admin/search_inplace?search=' + $('#search-field').val()
    }).then(function (r) {
        console.log(r);
        $('#page-container').html(r);
    });
};

$('#search-field').change(search);
$('#search-field').keyup(search);
// })();