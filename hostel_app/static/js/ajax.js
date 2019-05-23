$(document).ready(function(){
	 function getCookie(name) {
		 var cookieValue = null;
		 var i = 0;
		 if (document.cookie && document.cookie !== '') {
			 var cookies = document.cookie.split(';');
			 for (i; i < cookies.length; i++) {
				 var cookie = jQuery.trim(cookies[i]);
				 // Does this cookie string begin with the name we want?
				 if (cookie.substring(0, name.length + 1) === (name + '=')) {
				 	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				 	break;
			 		}
			 }
		 }
		 return cookieValue;
 	}
 	var csrftoken = getCookie('csrftoken');
 	function csrfSafeMethod(method) {
		 // these HTTP methods do not require CSRF protection
		 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		 }
	 $.ajaxSetup({
		 crossDomain: false, // obviates need for sameOrigin test
		 beforeSend: function(xhr, settings) {
			 if (!csrfSafeMethod(settings.type)) {
			 	xhr.setRequestHeader("X-CSRFToken", csrftoken);
			 }
		 }
	});	


	$(".form-control").on('keyup',function(){
		var val = $(".form-control").val(); 
		$.ajax({
				type: "GET",
				q: val,
				url: '/search/?name='+val,
				success: function( data ) {	
					$('.item-object').remove();
					for (var subject of data.subjects) {					
                    var describe = $("<div></div>");
                    describe.addClass('caption');
                    describe.append("<h4 class='pull-right'>₽"+subject.price+"</h4>");
                    describe.append("<h4><a href='/products/"+subject.id+"'>"+subject.name+"</a></h4>");
                    describe.append("<p>"+subject.description+"</p>");
                    var thumb = $("<div></div>");
                    thumb.addClass('thumbnail');
                    thumb.append("<img src='/static/"+subject.image+"' alt=''>");
                    thumb.append(describe);
                    var item = $('<div></div>');
                    item.addClass("col-sm-4 col-lg-4 col-md-4 item-object");
                    item.append(thumb);
                    $('.row-main').append(item);
					}									
				}
			});		
	});
});
