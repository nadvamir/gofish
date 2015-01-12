var API = "http://sjakobsen.pythonanywhere.com/gofish/api/" // Root URL for API commands

function getObjectFromAPI(url) {
    $.getJSON( url, function( data )
    {
        var toReturn = $.parseJSON(data);
        return toReturn;
    });
}

function getJSONFromAPI(url) {
    $.getJSON( url, function( data )
    {
        return data;
    });
}
