// returns the request
function drawData(request, params) {
    $.getJSON('/charts/api/get_data/', request, function(data) {
        console.log(data);
        if (!data.error) {
            drawChart(params, data.data);
        } else {
            alert(data.error);
        }
    });
}
