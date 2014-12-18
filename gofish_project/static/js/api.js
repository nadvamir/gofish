// sends a request for data draws the line chart
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

// sends a request for aggregated data and draws the bar chart
function drawBarData(request) {
    $.getJSON('/charts/api/get_bar_data/', request, function(data) {
        console.log(data);
        if (!data.error) {
            data = transformBarData(data.data);
            drawBarChart(data);
        } else {
            alert(data.error);
        }
    });
}

// sends a request for aggregated data and draws the box chart
function drawBoxData(request) {
    $.getJSON('/charts/api/get_box_data/', request, function(data) {
        console.log(data);
        if (!data.error) {
            data = transformBoxData(data.data);
            drawBoxChart(data, 'chart-div2');
        } else {
            alert(data.error);
        }
    });
}

// transforms bar chart data
function transformBarData(data) {
    return data.map(function(el) { return [el.x, el.id__count]; });
}

// transforms box chart data
function transformBoxData(data) {
    var hash = {};
    data.forEach(function(el) { 
        if (!!hash[el.x]) {
            hash[el.x].push(el.y);
        } else {
            hash[el.x] = [el.y];
        }
    });

    var data = [];
    for (var k in hash) {
        var vals = hash[k];
        vals.sort(function(a, b) { return a - b; });
        data.push([parseInt(k, 10), vals[0], vals[Math.floor(vals.length / 4)], vals[Math.floor(vals.length / 4) * 3], vals[vals.length-1]]);
    }
    console.log(data);
    return data;
}
