// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Callbacks that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

// line chart
function drawChart(params, result, divId) {
    divId = divId || 'chart-div';
    
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
    var chart = new google.visualization.LineChart(document.getElementById(divId));
    chart.draw(data, options);
}

// bar chart
function drawBarChart(result, divId) {
    divId = divId || 'chart-div';
    
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'x');
    data.addColumn('number', '#');
    data.addRows(result);
    
    var chart = new google.visualization.ColumnChart(document.getElementById(divId));
    chart.draw(data, {});
}

// box chart
function drawBoxChart(result, divId) {
    divId = divId || 'chart-div';
    
    // Create the data table.
    var data = new google.visualization.DataTable();
    console.log(result);
    data.addColumn('number', 'x');
    data.addColumn('number', 'min');
    data.addColumn('number', '1st-q');
    data.addColumn('number', '3rd-q');
    data.addColumn('number', 'max');
    data.addRows(result);
    
    var chart = new google.visualization.CandlestickChart(document.getElementById(divId));
    chart.draw(data, {legend: 'none'});
}
