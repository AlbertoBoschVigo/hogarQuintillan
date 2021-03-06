document.addEventListener('DOMContentLoaded', function (){
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    var ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
    //ReconnectingWebSocket()//
    setTimeout(function() {
        window.scrollTo(0, 1);
    }, 2000);
    const chatSocket = new WebSocket(
        ws_scheme
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.users){
            document.getElementById("listaUsuarios").innerHTML = "";
            data.users.forEach(elemento => {
                var ul = document.getElementById("listaUsuarios");
                var li = document.createElement("li");
                var inf = document.getElementById("infoChat").dataset.user;
                const aTag = document.createElement('a');
                //console.log(elemento);
                aTag.appendChild(document.createTextNode(elemento));
                aTag.setAttribute("id", elemento);
                aTag.setAttribute("href","javascript:void(0)"); 
                aTag.setAttribute("onclick", `privadoEnlace("${elemento}");`);
                //aTag.setAttribute("class", "badge badge-secondary enlace-chat");
                if (elemento == inf){
                    aTag.className = "badge badge-dark enlace-usuario";
                }
                else{
                    aTag.className = "badge badge-light enlace-usuario";
                }
                
                li.appendChild(aTag);
                ul.appendChild(li);
            });
            if(data.chats){
                document.getElementById("listaCanales").innerHTML = "";
                data.chats.forEach(elemento => {
                    var ul = document.getElementById("listaCanales");
                    var li = document.createElement("li");
                    var inf = document.getElementById("infoChat").dataset.canal;
                    const aTag = document.createElement('a');
                    aTag.appendChild(document.createTextNode(elemento.replace("chat_", "")));
                    aTag.setAttribute("id", elemento);
                    aTag.setAttribute("href", window.location.protocol + "//" + window.location.host + "/chat/" + elemento.replace("chat_", ""));
                    //aTag.setAttribute("class", "badge badge-secondary enlace-chat");
                    if (elemento == inf){
                        aTag.className = "badge badge-dark enlace-chat";
                    }
                    else
                    {
                        aTag.className = "badge badge-info enlace-chat";
                    }
                    
                    li.appendChild(aTag);
                    ul.appendChild(li);
                });
            }
        }
        else if(data.chats){
            document.getElementById("listaCanales").innerHTML = "";
            data.chats.forEach(elemento => {
                var ul = document.getElementById("listaCanales");
                var li = document.createElement("li");
                var inf = document.getElementById("infoChat").dataset.canal;
                const aTag = document.createElement('a');
                aTag.appendChild(document.createTextNode(elemento.replace("chat_", "")));
                aTag.setAttribute("id", elemento);
                aTag.setAttribute("href", window.location.protocol + "//" + window.location.host + "/chat/" + elemento.replace("chat_", ""));
                //aTag.setAttribute("class", "badge badge-secondary enlace-chat");
                if (elemento == inf){
                    aTag.className = "badge badge-dark enlace-chat";
                }
                else
                {
                    console.log('pues no');
                    aTag.className = "badge badge-info enlace-chat";
                }
                li.appendChild(aTag);
                ul.appendChild(li);
            });

        }
        else{
            document.querySelector('#chat-log').value += (data.hour + ' (' + data.user + '): ' + data.message + '\n');
            document.querySelector('#chat-message-input').focus();
        }
        
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