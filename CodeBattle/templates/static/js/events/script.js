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


var timeArray = []

function check_state() {  
    $.getJSON("/events/api", (json) => {
        if(json !== null){
            for( let i = 0; i < json.length; i++)
            {
                $(".card--main-button").each(function (index, el) {
                    let id = $(el).data('id');
                    console.log(id);
                    console.log(json[i].event_id.toString());
                    if(json[i].event_id == id && json[i].accepted == true) {
                        $(el).addClass('accepted');
                        $(el).text('Отменить заявку');
                    }
                });

                timeArray.push( {'id' : json[i].event_id, 'time' : new Date(json[i].time)} )
            }

            ///////////////////
            setInterval(timer, 1000)
        }
    })
}
$(document).ready(function () {
    function onEventClick(e){
        id = $(e).data('id');
        // if($(e).hasClass('event-grid--item'))
            window.location.href = "/battle/"+id;
    }
    
    function set_event_click(){
        $('.enter').each(function (index,el) {
    
            $(el).css('cursor', 'pointer');
    
            $(el).click(function (e) { 
                e.preventDefault();
                
                let id = $(el).data('id');
                window.location.href = "/battles/"+id;
               })
            // el.addEventListener("click",onEventClick);
        })
    }
    
    function accept_event() {
        $('.event-grid--apply').each(function (index, el) { 
             $(el).click(function (e) { 
                 e.preventDefault();
                 
                console.log(1); 
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

    accept_event();
    check_state();
    set_event_click();
});


function timer() {

    timeArray.forEach((elem) => {
        $(".card--time-text").each(function(index, timeTag) {

            if ($(timeTag).data('id') == elem.id) {
                let curtime = Date.now();
            
                if (curtime > elem.time || curtime == elem.time) {
                    timeArray.splice(timeArray.indexOf(elem),1)

                    // let enter_button = null;
                    // $('.hidden').each(function(index, btn) {
                    //     if ($(btn).data('id') == elem.id) {
                    //         enter_button = $(btn);
                    //     }
                    // })
                    // enter_button.css("display","none")

                } else {
                    let time = elem.time - curtime;
                    let secs = Math.trunc(time / 1000 % 60 );
                    let mins = Math.trunc(time / 1000 / 60);
                    let hours = Math.trunc(time / 1000 / 360);
                    
                    let enter_button = null;
                    $('.hidden').each(function(index, btn) {
                        if ($(btn).data('id') == elem.id) {
                            enter_button = $(btn);
                        }
                    })

                    let accept_button = null;
                    $('.accept').each(function(index, btn) {
                        if ($(btn).data('id') == elem.id) {
                            accept_button = $(btn);
                        }
                    })

                    if (hours == 0 && mins < 5 && enter_button.css("display") == "none") {
                        accept_button.css("display", "none")
                        enter_button.css("display", "block")
                        
                    }


                    if (secs < 10) secs = "0" + secs;
                    if (mins < 10) mins = "0" + mins;
                    if (hours < 10) hours = "0" + hours;

                    $(timeTag).html("До начала осталось: " + hours + ":" + mins + ":" + secs);
                }
            }
        })
    })

}