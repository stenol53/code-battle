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


console.log("SOCKET JS INCLUDED");
moment.locale('ru');

var user_id, battle_id

$(document).ready(function () {

    user_id = $("#user_id").val()
    battle_id = $("#battle_id").val()
    var date;
    console.log(battle_id)
    $.ajax({
        type: "POST",
        url: "/battles/user_validate/",
        data: {
            'battle_id': battle_id    
        },
        dataType: "json",
        success: function (response) {
            if(response.response == 1) {
                // date = new Date(response.start_at);
                // if(date > Date.now()) {
                //     console.log("Еще не началось");
                //     $(".content").append("<h2 id=\"text\">Событие еще не началось</h3>");
                //     $(".content").append("<h3 id=\"time\">До начала события " + moment(date).fromNow() + "</h3>");
                //     var interval = setInterval(()=>{
                //         if (date > Date.now()) {
                //             $("#time").text("До начала события " + moment(date).fromNow());
                //         } else {
                //             startWork();
                //             clearInterval(interval);
                //         }
                //     },1000);
                // } else {
                //     console.log("событие уже прошло")
                // }

                startWork();
            } else {
                alert("Вы не принимаете участие в этой битве.");
                console.log("BAD VALIDATING");
            }
        }
    });



    function startWork(){
        /////Начало сеанса
        $("#text").text("Начинаем событие");
        $("#time").remove();
        startSocket();
        
    }




/////////////////////////////

    function startSocket() {
        console.log(window.location)
        var loc = window.location;

        var wsStart = "ws://"
        if(loc.protocol == "https:")
            wsStart = "wss://"
        var endpoint = wsStart + loc.host + loc.pathname
        console.log(endpoint)
        var socket = new WebSocket(endpoint)


        socket.onmessage = function (e) {
            console.log('message',e);
        }

        socket.onopen = function (e) {
            console.log('open',e);
            $("#readybtn").click(function (e) { 
                e.preventDefault()
                socket.send(JSON.stringify({
                    'type' : 'ready',
                    'id' : user_id,
                    'battle_id' : battle_id,
                    'ready': true
                }))    

                $(e.target).remove()
                $('.wait-main-container').css("display", "flex")
            });
        }

        socket.onerror = function (e) {
            console.log('error',e);
        }

        socket.onclose = function (e) {
            console.log('close',e);
        }
    }

});
