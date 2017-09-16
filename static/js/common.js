$(function() {

	// lessons ajax
	var offset = 10;
	$(window).scroll(function() {
		if($(window).scrollTop() + $(window).height() == $(document).height()) {
			$.get('/student_lessons_ajax/', {offset: offset}, function(data) {
                $('.lessons').delay(1500).append(data);
            });
			offset = offset + offset;
		}
	});

	// User menu
	$('#profile-link').on('click', function(e) {
		e.stopPropagation();
		e.preventDefault();
		$(this).toggleClass('active');
		$('#profile-dropdown').toggleClass('shown');
	});
	$(document).on('click', function() {
		$('#profile-link').removeClass('active');
		$('#profile-dropdown').removeClass('shown');
	});

	//Slidebar
	var controller = new slidebars();
	controller.init();
	$('#toggle-m-menu').on('click', function(e) {
		e.stopPropagation();
		e.preventDefault();
		controller.toggle('m-menu');
	});
	$('.btn-close').on('click', function(e) {
		controller.close();
	});

	//SVG Fallback
	if(!Modernizr.svg) {
		$("img[src*='svg']").attr("src", function() {
			return $(this).attr("src").replace(".svg", ".png");
		});
	};

	//E-mail Ajax Send
	//Documentation & Example: https://github.com/agragregra/uniMail
	$("form").submit(function() { //Change
		var th = $(this);
		$.ajax({
			type: "POST",
			url: "mail.php", //Change
			data: th.serialize()
		}).done(function() {
			alert("Thank you!");
			setTimeout(function() {
				// Done Functions
				th.trigger("reset");
			}, 1000);
		});
		return false;
	});

	//Chrome Smooth Scroll
	try {
		$.browserSelector();
		if($("html").hasClass("chrome")) {
			$.smoothScroll();
		}
	} catch(err) {

	};

	$("img, a").on("dragstart", function(event) { event.preventDefault(); });
	
});

$(window).load(function() {

	$(".loader_inner").fadeOut();
	$(".loader").delay(400).fadeOut("slow");

});
