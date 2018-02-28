(function () {
    $('.ui.search').search({
        apiSettings: {
            url: '/admin/json_search?search={query}'
        },
        type: 'category'
    });
})();