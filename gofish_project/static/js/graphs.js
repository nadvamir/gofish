// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart(params, result) {
    console.log(params);
    // Create the data table.
    var data = new google.visualization.DataTable();
    for (var i in params.names) {
        data.addColumn('number', params.names[i]);
    }
    data.addRows(params.dataF(result));
    console.log(params.dataF(result));

    // Set chart options
    var options = {'title'  : params.title,
                   'width'  : 800,
                   'height' : 300};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('chart-div'));
    chart.draw(data, options);
}

