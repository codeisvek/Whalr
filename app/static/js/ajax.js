(function(){
	$('a[data-target=#userModal2]').click(function(){
		$.get('login', function(data)	{
			$('#userModal2').html(data);
		});
	});
})(jQuery)