// returns the request
function drawData(request) {
    $.getJSON('/charts/api/get_data/' + request, function(data) {
        console.log(data);
        if (!data.error) {
            drawChart(data);
        } else {
            alert(data.error);
        }
    });
}
