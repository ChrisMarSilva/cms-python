
$(document).ready(function () {

    $('#btn1').on('click', callEndpoint);

    $('#btn2').on('click', function () {
        callEndpoint();
    });

    // $.get('/data').done(function (results) {
    //     console.log('results', results.results);
    // });

})

function callEndpoint() {

    $.get('/data').done(function (results) {
        console.log('results', results.results);
    });

    $.ajax({
        type: 'POST',
        url: '/data',
        // data : { 'first': valueOne, 'second': valueTwo },
        success: function(results) {
            console.log(results)
        },
        error: function(error) {
            console.log(error)
        }
    });

}
