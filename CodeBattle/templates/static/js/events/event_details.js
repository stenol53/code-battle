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
                    const months = {
                        '01': 'Января',
                        '02': 'Февраля',
                        '03': 'Марта',
                        '04': 'Апреля',
                        '05': 'Мая',
                        '06': 'Июня',
                        '07': 'Июля',
                        '08': 'Августа',
                        '09': 'Сентября',
                        '10': 'Октября',
                        '11': 'Ноября',
                        '12': 'Декабря',
                    };

                    console.log(data);

                    const modal = document.querySelector('.info-window');
                    modal.style.display = 'flex';

                    if (data.photo) {
                        document.querySelector('.modal--image').src = data.photo;
                    }
                    document.querySelector('.card--title').textContent = data.title;

                    let [date, time] = data.date.split('T');
                    let [year, month, day] = date.split('-');
                    time = time.slice(0, time.length - 1);

                    document.querySelector('.card--time-text').textContent = `${day} ${months[month]} ${year} ${time}`;
                    document.querySelector('.card--text-section-text').textContent = data.text;
                    document.querySelector('.modal--status').textContent = data.status;
                    document.querySelector('.modal--count').textContent = data.users_count;
                    // const 

                });
        });
    });
}