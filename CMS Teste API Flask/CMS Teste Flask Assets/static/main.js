
$(document).ready(function () {

})

function callEndpoint() {

    $.get('/data').done(function (results) {
        console.log('results', results.results);
    });

    $.ajax({
        type: 'POST',
        url: '/data',
        success: function(results) {
            console.log(results)
        },
        error: function(error) {
            console.log(error)
        }
    });

}
