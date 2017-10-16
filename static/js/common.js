$(function() {

	// get student lessons ajax
	var offset = 10,
		btn = $('#show-more-lessons'),
		countLessons = btn.data('count');
	btn.on('click', function() {
		$.get('/student_lessons_ajax/', {offset: offset}, function(data) {
			$('.lessons').append(data);
		});
		offset = offset + 10;
		if (countLessons < offset) {
			btn.hide();
		}
	});

	// student page values ajax
	var button = $('#show-more-values');
	var count = parseInt(button.data('count')),
		username = button.data('username'),
		offsetStart = 5,
		offsetEnd = 10;

	button.on('click', function () {
		$.ajax({
			url: '/get_values_ajax/',
			data: {username: username, offsetStart: offsetStart, offsetEnd: offsetEnd},
			success: function (data) {
				$('.books').append(data);
				offsetStart = offsetStart + 5;
				offsetEnd = offsetEnd + 5;
				if (count < offsetStart) {
					button.hide();
				}
            }
		});
    });

	// ajax student list
	$('#lesson-add-student-search').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/student_search/', {starts_with: query}, function(data){
		$('#student-search').html(data);
		});
	});

	// add student in lesson
	var students_input = $('#id_students');

	$('#student-search').on('click', '.student-add', function (event) {
		var student_id = event.target.getAttribute('data-student_id');
		students_input.val(students_input.val() + ',' + student_id);
		var student = $('.l-srcr[data-student_id="'+ student_id + '"]');
		$('#student-list-header').hide();
		student.find('button').removeClass('student-add').addClass('student-delete').text('Убрать');
		student.appendTo('#students-list');
		console.log(students_input.val());
    });

	// delete student from lesson
	$('#students-list').on('click', '.student-delete', function (event) {
		var student_id = event.target.getAttribute('data-student_id');
		var students_list = students_input.val().replace(/(^,+|,+$)/g, "").split(",");
		for (var i = 0; i < students_list.length; i++) {
			if (students_list[i] == student_id) {
				students_list.splice(i, 1);
				break;
			}
		}
		if (students_list.length == 0) {
			$('#student-list-header').show();
		}
		students_input.val(students_list);
		event.target.closest(".l-srcr").remove();
		console.log(students_input.val());
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

$(window).ready(function() {

	$(".loader_inner").fadeOut();
	$(".loader").delay(400).fadeOut("slow");

});
