$(document).ready(function() {
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
                console.log(JSON.parse(data));
                btn.prop("disabled", true);
                setTimeout(function() {
                    btn.prop("disabled", false);
                }, (parseInt(JSON.parse(data)["cooldowntime"])) * 1000);
$("#userpoints").html(JSON.parse(data)["currentpoints"]);
$("#currentpoints").html(JSON.parse(data)["currentpoints"]);
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
	
	$.ajax({
		url:"/send_attack",
		contentType: "application/json",
		data:JSON.stringify(attackData),
		type: "PUT",
		success:function(data){
			console.log(JSON.parse(data));
		},
		error: function(){
			alert("error");
		}
	});
	});
});
