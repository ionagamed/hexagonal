(function () {
    const setMenuToSearch = function () {
        $('.item.active').removeClass('active');
        $('#menu-search-field-item').addClass('active');
    };

    const searchIntro = function (term) {
        if (!window.searchStateChanged) {
            window.searchStateChanged = true;
            if (window.history.pushState) {
                window.history.pushState("", "Hexagonal", '/admin/search?search=' + term);
            }
            setMenuToSearch();
        } else {
            if (window.history.replaceState) {
                window.history.replaceState("", "Hexagonal", '/admin/search?search=' + term);
            }
        }
    };

    const search = function (e) {
        const term = $('#search-field').val();
        const url = '/admin/search_inplace?search=' + term;
        searchIntro(term);
        $.ajax({
            url: url
        }).then(function (r) {
            $('#page-container').html(r);
        });
    };

    $('#search-field').change(search);
    $('#search-field').keyup(search);
})();