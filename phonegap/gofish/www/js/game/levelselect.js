$.getJSON( API+"getgame/", function( data ) {
	var money = data.player.money;
 	var levels = [];
 	$.each( data.levels, function( i, level ) {
    	levels.push( "<li id='" + i + "'>" + level.name + "</li>" );
 	});

 	$( "<div/>", {
 		"class": "hud",
 		html: "Money: "+money
 	}).appendTo( "body" );
 
 	$( "<ul/>", {
 		"class": "my-new-list",
		html: levels.join( "" )
	}).appendTo( "body" );
});