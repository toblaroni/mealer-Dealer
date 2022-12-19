function clearMessage(msg){
    let container = document.getElementsByClassName('message-container')
    container[0].style.display = 'none'

}

// Ajax function for saving meal deals
$(document).ready(function () {
    let csrf_token = $('meta[name=csrf-token]').attr('content')
    // Add the token to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("a.save-meal").on("click", function() {
        // Get the meal ID
        let mealId = $(this).attr('id')
        let likesSpan = document.getElementById(mealId)

        $.ajax({
            // Make up the header
            url: '/saveMealDeal',
            type: 'POST',
            data: JSON.stringify({ MealId: mealId }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",

            success: function(response){
                if(response.saved == false){
                    // If it isn't saved up the likes
                    likesSpan.innerHTML = "Likes " + response.likes
                } else {
                    alert('This meal is already in your collection')
                }
            },
            error: function(error){
                console.log(error)
            }
        })
    })
})