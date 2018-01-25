$(document).ready(function() {

$(".events").slice(0,4).show();	
$("#loadmore").click(function(e){
	$(".events:hidden").slice(0,4).show()
});	
	
	$('#pointsButton').click(function(e) {
    var btn = $(this);
        e.preventDefault();
        var now = new Date().getTime();
        var formData = {
            'time': String(now)
        };    
		    
	$.ajax({
            url: '/add_points',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            type: 'PUT',
            success: function(data) {
            responseData = JSON.parse(data);
		console.log(responseData);
                btn.prop("disabled", true);
                setTimeout(function() {
                    btn.prop("disabled", false);
                }, (parseInt(responseData["cooldowntime"])) * 1000);
	document.getElementById(responseData["userpoints"]).innerHTML = (responseData["currentpoints"]);
	document.getElementById(responseData["userlistpoints"]).innerHTML = (responseData["currentpoints"]);
            },
            error: function() {
                alert("you're still in cooldown. wait.");
            }
        });
    });

var users_affected = [];
var ability_used = "";
	$('[name="abilityButtons"]').each(function(){
		$(this).click(function(){	
			ability_used = $(this).attr('id');
		});
	});

	$('[name="userButtons"]').each(function(){
		$(this).click(function(){
			if ($(this).is(":checked")==false){
				users_affected.splice([users_affected.indexOf($(this).attr('id'))],1);

			}else{
				users_affected.push($(this).attr('id'));
			}
		});
	});

$("#fireButton").click(function(e){	
	var attackData = {
		'users_affected' : users_affected,
		'ability_used' : ability_used
	};

	console.log(attackData)
	
	$.ajax({
		url:"/send_attack",
		contentType: "application/json",
		data:JSON.stringify(attackData),
		type: "PUT",
		success:function(data){
			result = JSON.parse(data);
			$.each(result, function(k,v){
				if (document.getElementById(k+"listpoints") != null){
				document.getElementById(k+"listpoints").innerHTML = (v);
				}
				console.log(k + ' : ' +v);
			});
			alert(result["result"]);
		},
		error: function(){
			alert("error");
		}
		});
	});

});
