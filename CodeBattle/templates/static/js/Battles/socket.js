console.log("SOCKET JS INCLUDED");

$(document).ready(function () {
    
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
    }

    socket.onerror = function (e) {
        console.log('error',e);
    }

    socket.onclose = function (e) {
        console.log('close',e);
    }
});
