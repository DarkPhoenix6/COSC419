
function form_state_field(){
    if ($("#country").val() === "CA"){
        $("#state").prev().text("Province");
        $("#state").next().text("Please provide a valid province.");
        $("#zip").prev().text("Postal Code");
        $("#zip").next().text("Postal code required.");
    } else if ($("#country").val() === "US"){
        $("#state").prev().text("State");
        $("#state").next().text("Please provide a valid state.");
        $("#zip").prev().text("Zip Code");
        $("#zip").next().text("Zip code required.");
    }
}

$( document ).ready( function () {
    $("#country").on("click", form_state_field);
    $("#country").on("change", form_state_field);
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
$( document ).ready( function() {
    'use strict';

    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');

        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
});

