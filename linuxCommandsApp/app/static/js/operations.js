$(function(){

    $("#action").on('change', function(){
        if($(this).val() === "delete"){
        $("#inputPassword").hide();
        }
        else{
         $("#inputPassword").show();
        }
    });
	$('#btn').click(function(){
      var action =   $('#action').val();
      if (action == 'create'){
		$.ajax({
			url: '/createUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
			    var resp = JSON.parse(response)
			    alert(resp.message)
				console.log(response);
			},
			error: function(error){
			    alert('fail')
				console.log(error);
			}
		})
	}
	else if (action == 'delete'){
	$.ajax({
			url: '/deleteUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
			    var resp = JSON.parse(response)
			    alert(resp.message)
				console.log(response);
			},
			error: function(error){
			    alert('fail')
				console.log(error);
			}
		})


	}
});
});