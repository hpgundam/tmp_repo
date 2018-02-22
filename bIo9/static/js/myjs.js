$(document).ready(function(){
	$(".messages").fadeOut(3000);
	
	$('.active_user_outline').hover(
			function(){
			$(this).find('p').show();
		}, function(){
			$(this).find('p').hide();
		});
});