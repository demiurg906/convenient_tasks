$('#search-button').click(function () {
    window.location.href = window.location.origin + '/task/' + $('#search-input').val();
});