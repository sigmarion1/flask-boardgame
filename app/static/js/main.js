var input_field = document.getElementById('messagein');
var chat_field = document.getElementById('chat');
var chat_body = document.getElementById('cb');


// create a random username
var username = 'user' + parseInt(Math.random() * 10000);

var socketio = io.connect(location.origin + '/nicklogin',
//    {query: 'username=' + username, 'transports': ['websocket']});
    {query: 'username=' +'한글', 'transports': ['websocket']});


// event handler when ENTER is pressed on the chat input field
input_field.onchange = function() {
    socketio.emit('post-message', { message: this.value });
    this.value = '';
}

// the server is sending a message to display in the chat window
socketio.on('message', function(message) {
    msg = document.createElement('div');
    if (message.type == 'chat') {
	    // this is a message written by other user
	msg.className = "message-item";
        msg.innerHTML = '<div class="message-content">' + message.user + ' : ' + message.message + '</div>' +
            '<div class="message-action">' + message.time + '</div>';
    }
    else if (message.type == 'chat_self') {
        	    // this is a message written by other user
	msg.className = "message-item outgoing-message";
        msg.innerHTML = '<div class="message-content">' + message.message + '</div>' +
            '<div class="message-action">' + message.time + '</div>';

    }
    else if (message.type == 'system') {
	    // this is a control message that comes from the server itself
	msg.className = "message-item system";
	msg.innerHTML = '<div class="message-content">' + message.message + '</div>' +
		    '<div class="message-action">' + message.time + '</div>';
    }

    chat_field.appendChild(msg);
    chat_body.style.overflow = 'auto'
	chat_body.scrollTop = chat_body.scrollHeight; // scroll to bottom
}); 

input_field.focus();
