document.addEventListener('DOMContentLoaded', function (){
    const roomName = JSON.parse(document.getElementById('room-name').textContent);

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        document.querySelector('#chat-log').value += (data.hour + ' (' + data.user + '): ' + data.message + '\n');
        document.querySelector('#chat-message-input').focus();
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-log').style.animationPlayState = 'running';
    setTimeout(function(){ 
        document.querySelector('#chat-log').style.animationPlayState = 'paused';
        //console.log(textarea.style.animationPlayState);
    }, 2000);
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            e.preventDefault();
            e.stopPropagation();
            document.querySelector('#chat-message-submit').click();
            
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
})
$(document).ready(function(){
    $('#exampleModal').on('shown.bs.modal', function () {
        $('#message-text').trigger('focus');
        $('#message-text').val("");
        $('#mensajeInvalido').text("");
    });
    $( '#exampleModal' ).on( 'keypress', function( e ) {
        if( e.keyCode === 13 ) {
            e.preventDefault();
            $('#btnFormOpinion').click();
        }
    } );
});

function cambiarChat() {
    var form = document.querySelector('.needs-validation');
    const elinput = document.querySelector('#message-text');
    const nuevoCanal = elinput.value;
    if (!elinput.checkValidity()) {
        //console.log('No es valido');
        document.getElementById("mensajeInvalido").innerHTML = elinput.validationMessage;
        elinput.value = "";
        elinput.focus();
    }
    else{
        $('#exampleModal').modal('hide');
        //console.log('Parece valido');
        window.location.pathname = '/chat/' + nuevoCanal + '/';
    }
    
    
};