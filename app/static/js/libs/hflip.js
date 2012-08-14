$(document).ready(function(){
var margin =$(".image1").width()/2;
var width=$(".image1").width();
var height=$(".image1").height();
$(".image2").stop().css({width:'0px',height:''+height+'px',opacity:'0.5'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$(".image1").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0.5'},{duration:250});
		var self = this;
		window.setTimeout(function() {
			//$(self).stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:250});
			$(self).parent().find('.image2').animate({width:''+width+'px',height:''+height+'px',opacity:'1'},{duration:250});
		},500);
	});
	$(".image2").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',opacity:'0.5'},{duration:250});

		var self = this;
		window.setTimeout(function() {
			//$(self).stop().animate({width:''+width+'px',height:''+height+'px',opacity:'1'},{duration:250});
			$(self).parent().find('.image1').animate({width:''+width+'px',marginLeft: "0px", height:''+height+'px',opacity:'1'},{duration:250});
		},500);
	});


	$(".grid-item").click(function(e){

	})
});

