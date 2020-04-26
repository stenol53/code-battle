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

        var curQuestionID = 1;
        var curMessage = "";
        var answerVariants = [];
        var answerEndDate;


        socket.onmessage = function (e) {
            console.log('message',e);
            
            let jsn = JSON.parse(e.data)

            if(jsn["type"] == "session") {
                if(jsn["id"] != user_id)
                {
                    socket.send(JSON.stringify({
                        'type' : 'session',
                        'id' : jsn["id"],
                        'start_session' : true
                    }))
                }

                if(jsn["start_session"] == true){ //СТАРТАНУЛИ ВОПРОСЫ

                    $("#readyBtn").replaceWith("<h1>НАЧИНАЕМ БЛЯ<h2>");
                    socket.send(JSON.stringify({
                        'type': 'question',
                        'method': 'next',
                        'id': user_id,
                        'question_num': curQuestionID
                    }))
                }
            } else if(jsn["type"] == "question") {
                if(jsn["method"] == "new") { //ПРИШЕЛ НОВЫЙ ВОПРОС

                        console.log(jsn);
                    curMessage = jsn["message"]
                        console.log(curMessage);
                    var json = jsn["answer_variant"]
                        console.log(json);
                    
                    json.forEach(element => {
                        answerVariants.push(element)
                    });
                    answerEndDate = Date(jsn["answer_end_date"])


                }
                console.log(curMessage);
                console.log(answerVariants);
                console.log(answerEndDate);
            }

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

                // $(e.target).css("display", "none")
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
