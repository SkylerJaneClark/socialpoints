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
                alert("error");
            }
        });
    });
	$('[name="abilityButtons"]').each(function(){
		$(this).click(function(){	
			console.log($(this).hasClass("active"));
		});
	});

	$('[name="userButtons"]').each(function(){
		$(this).click(function(){
			console.log($(this).is(":checked"));
		});
	});
	$("#fireButton").click(function(e){
		console.log("ATTACK")
	});
});
