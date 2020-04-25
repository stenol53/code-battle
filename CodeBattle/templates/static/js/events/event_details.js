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

const closeInfoWindow = document.querySelector('.close-info-button');

closeInfoWindow.addEventListener('click', () => {
    document.querySelector('.info-window').style.display = 'none';
});

function accept_event() {
    $('.card--secondary-button').each(function(index, el) {
        $(el).click(function(e) {
            e.preventDefault();

            let id = $(el).data('id');

            $.get("/events/event_details/", { event_id: id })
                .done(function(data) {
                    // ПИШИ КОД ТУТ

                    console.log(data);

                    const modal = document.querySelector('.info-window');
                    modal.style.display = 'flex';

                    document.querySelector('.card--title').textContent = data.title;
                    document.querySelector('.card--time-text').textContent = data.date;
                    document.querySelector('.card--text-section-text').textContent = data.text;
                    document.querySelector('.modal--image').src = data.photo;
                    document.querySelector('.modal--status').textContent = data.status;
                    document.querySelector('.modal--count').textContent = data.users_count;
                    // const 

                });
        });
    });
}