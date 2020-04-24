// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
///////////////////////////////////////////////


function accept_event() {
    console.log(111);
    $('.card--main-button').each(function (index, el) { 
        console.log(333);
         $(el).click(function (e) { 
             e.preventDefault();
             
            let id = $(el).data('id');

            if($(e.target).hasClass('accepted')){
                $.ajax({
                    type: "POST",
                    url: "/events/deny/",
                    data: {
                        'event_id': id
                    },
                    dataType: "json",
                    success: function (response) {
                        $(el).removeClass('accepted');
                        $(el).text("Подать заявку");
                    }
                });
            } else {
                $.ajax({
                    type: "POST",
                    url: "/events/accept/",
                    data: {
                        'event_id': id
                    },
                    dataType: "json",
                    success: function (response) {
                        $(el).addClass('accepted');
                        $(el).text("Отменить заявку");
                    }
                });
            }

         });
    });
}

function check_state() {  
    $.getJSON("/events/api", (json) => {
        if(json !== null){
            for( let i = 0; i < json.length; i++)
            {
                $(".card--main-button").each(function (index, el) {
                    let id = $(el).data('id');
                    console.log(id);
                    console.log(json[i].event_id.toString());
                    if(json[i].event_id == id) {
                        $(el).addClass('accepted');
                        $(el).text('Отменить заявку');
                    }
                });
            }
        }
    })
}


$(document).ready(function () {
    accept_event();
    check_state();
});