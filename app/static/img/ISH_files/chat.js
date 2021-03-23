chat_message_template_left = `
    <li class="message">
        <div class="avatar"></div>
        <div class="text_wrapper"><div class="text"></div></div>
    </li>`

chat_message_template_right = `
    <li class="message">
        <div class="avatar"></div>
        <div class="text_wrapper"><div class="text"></div></div>
    </li>`

function Message(arg) {
    this.text = arg.text;
    this.side = arg.side;
    this.name = arg.name
    this.initials = arg.initials;
    this.messages = arg.messages
    this.draw = function (_this) {
        return function () {
            var $message;
            if (_this.side === "left") {
                $message = $(chat_message_template_left);
            } else {
                $message = $(chat_message_template_right);
            }
            $message.addClass(_this.side).find('.text').html(_this.text);
            $message.find('.avatar').html(_this.name);
            $message.attr("title", _this.name);
            _this.messages.append($message);
            _this.messages.scrollTop(_this.messages.prop('scrollHeight'));
        };
    }(this);
    return this;
}


class Chat {
    rooms = {}

    constructor() {
        socketio.subscribe_on_receive("chat-line", this.socketio_receive_chat_line_cb.bind(this));
    }

    start(user_code) {
        socketio.start(null, user_code);
    }

    subscribe_to_room(room_code, sender_code, user_name, user_initials) {
        socketio.subscribe_to_room(room_code);
        this.rooms[room_code] = {
            sender_code: sender_code,
            name: user_name,
            initials: user_initials,
            jq_send_button: $("#" + room_code).find(".send_message"),
            jq_input_text: $("#" + room_code).find(".message_input"),
            jq_output_messages: $("#" + room_code).find(".messages")
        };

        this.rooms[room_code].jq_send_button.on("click", {value: room_code}, function (e) {
            var room_code = e.data.value;
            return this.send_chat_line(room_code, this.rooms[room_code].sender_code, this.rooms[room_code].name, this.rooms[room_code].initials, this.rooms[room_code].jq_input_text);
        }.bind(this));

        this.rooms[room_code].jq_input_text.on("keyup", {value: room_code}, function (e) {
            if (e.which === 13) {
                var room_code = e.data.value;
                return this.send_chat_line(room_code, this.rooms[room_code].sender_code, this.rooms[room_code].name, this.rooms[room_code].initials, this.rooms[room_code].jq_input_text);
            }
        }.bind(this));
    }

    send_chat_line(room_code, sender_code, name, initials, $jq_input_element = null, text = null) {
        if ($jq_input_element) {
            text = $jq_input_element.val();
            $jq_input_element.val("");
        }
        if (text.trim() === "") return;
        socketio.send_to_server('chat-line', {
            room: room_code,
            sender: sender_code,
            name: name,
            initials: initials,
            text: text
        });
        return false;
    }

    chat_history = function (history) {
        var _this = this;
        history.forEach(function (v) {
            _this.add_chat_line(v.room, v.sender, v.text, v.name, v.initials);
        });
    }.bind(this);

    socketio_receive_chat_line_cb = function (type, data) {
        this.add_chat_line(data.room, data.sender, data.text, data.name, data.initials)
    }.bind(this);

    add_chat_line(room, sender, text, name, initials) {
        if (this.rooms[room]) {
            var message = new Message({
                text: text,
                side: room == sender ? 'left' : 'right',
                name: name,
                initials: initials,
                messages: this.rooms[room].jq_output_messages
            });
            message.draw();
        }
    }

    // Scroll to bottom of chat when displayed
    add_dummy_line() {
        $(".messages").append("  ");
        $(".messages").scrollTop(100000);
    }
}

var chat;
$(function () { // same as $(document).ready()
    chat = new Chat();
});

