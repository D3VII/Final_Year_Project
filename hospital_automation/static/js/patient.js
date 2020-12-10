function receive_patient() {
    $.get('api/receive_incoming_patient', function (data) {
        console.log(data)
        for (var patient in data){
            var patient_id = data[patient]["id"];
            var name = data[patient]["first_name"];
            var lname = data[patient]["last_name"];
            current_html = $('#board').html();
            var para = document.createElement("div");
            $(para).append('<a href="/doctor/'+ patient_id +'"><div class="card-container" ><div id="'+patient_id+'" class="card">'+'<div class = "container">'+ name + " " + lname + '</div></div></div></a>');
            current_html += $(para).html();
            $('#board').html(current_html);
        }
    })
}

function incoming_patient_to_dispensary(){
    $.get('api/receive_incoming_patient_to_dispensary', function (data) {
        console.log(data)
        for (var patient in data){
            var patient_id = data[patient]["id"];
            var name = data[patient]["first_name"];
            var lname = data[patient]["last_name"];
            current_html = $('#board').html();
            var para = document.createElement("div");
            $(para).append('<a href="/dispensary/'+ patient_id +'"><div class="card-container" ><div id="'+patient_id+'" class="card">'+'<div class = "container">'+ name + " " + lname + '</div></div></div></a>');
            current_html += $(para).html();
            $('#board').html(current_html);
        }
    })
}

function incoming_patient_for_test(){
    $.get('api/receive_incoming_patient_for_test', function (data) {
        console.log(data)
        for (var patient in data){
            var patient_id = data[patient]["id"];
            var name = data[patient]["first_name"];
            var lname = data[patient]["last_name"];
            current_html = $('#board').html();
            var para = document.createElement("div");
            $(para).append('<a href="/test/'+ patient_id +'"><div class="card-container" ><div id="'+patient_id+'" class="card">'+'<div class = "container">'+ name + " " + lname + '</div></div></div></a>');
            current_html += $(para).html();
            $('#board').html(current_html);
        }
    })
}
