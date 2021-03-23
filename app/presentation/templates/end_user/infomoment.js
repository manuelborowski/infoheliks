var formio;
var panel_components = [];
$(document).ready(function () {
    const formOptions = {
        sanitizeConfig: {
            addTags: ['iframe'],
            addAttr: ['allow'],
            ALLOWED_TAGS: ['iframe'],
            ALLOWED_ATTR: ['allow']
        },
    }
    Formio.createForm(document.getElementById('infosession-form'), template, formOptions).then((form) => {
        formio = form;
        $.each(default_values, function (k, v) {
            try {
                form.getComponent(k).setValue(v);
            } catch (error) {
                return;
            }
        });
        $('.formio-component-panel').on('click', panel_header_clicked);
        $('.nav-link').on('click', panel_header_clicked);
        $(".chat_window").parent().parent().parent().css("min-height", "600px");
        set_tabs_visibility(0, false);
        chat.start(user["registration-code"]);
        $(".chat_window").each(function (d, v) {
            chat.subscribe_to_room(v.id, user["registration-code"], user.full_name, user.initials);
        });
        chat.chat_history(default_values.chat_history);
        set_stage_showtime(2, default_values.stage_2_showtime);
        set_stage_showtime(3, default_values.stage_3_showtime);
        set_stage_showtime(4, default_values.stage_4_showtime);
        if (user.is_guest) {
            set_popup_message_timeout(default_values.stage_3_showtime);
        }
        $(".formio-component-panel").each(function(i, c) {
            key = "key-" + c.className.split('component-key-')[1]
            panel_components.push(key);
        });
        if (default_values.enter_site_popup != '') {
            show_message_popup(default_values.enter_site_popup);
        }
        $(".wonder-link").on("click", function() {
            console.log("wonder clicked");
            socketio.send_to_server("enter-wonder-room", {"code": user["registration-code"]})
        });
    });
});


function set_tabs_visibility(stage, visible) {
    if (stage === 2) {
        if (visible) {
            $("[href='#tab-clb']").css("display", "block")
            $("[href='#tab-scholengemeenschap']").css("display", "block")
            $("[href='#tab-internaat']").css("display", "block")
        } else {
            $("[href='#tab-clb']").css("display", "none")
            $("[href='#tab-scholengemeenschap']").css("display", "none")
            $("[href='#tab-internaat']").css("display", "none")
        }
    }
    if (stage === 3) {
        if (visible) {
            $("[href='#tab-scholenbeurs']").css("display", "block");
        } else {
            $("[href='#tab-scholenbeurs']").css("display", "none");
        }
    }
    if (stage === 4) {
        if (visible) {
            $("[href='#tab-scholengemeenschap-coworker']").css("display", "block")
        } else {
            $("[href='#tab-scholengemeenschap-coworker']").css("display", "none")
        }
    }
    if (stage === 0) {
        set_tabs_visibility(2, visible);
        set_tabs_visibility(3, visible);
        set_tabs_visibility(4, visible);
    }
}

function set_stage_showtime(stage, showtime_string) {
    var now = new Date();
    var showtime = new Date(showtime_string);
    var delta = showtime - now;
    if (delta < 0) {
        delta = 0;
    }
    setTimeout(set_tabs_visibility, delta, stage, true);
}


function set_popup_message_timeout(showtime_string) {
    var now = new Date();
    var showtime = new Date(showtime_string);
    var delta = showtime - now;
    if (delta < 0) {
        delta = 0;
    }
    setTimeout(show_message_popup, delta, "De scholenbeurs is nu open");
}


function show_message_popup(message) {
    $("#messageModal .modal-title").html(message)
    $("#messageModal").modal();
}


var magnificPopupConfig = {
    type: 'iframe',
    iframe: {
        patterns: {
            googledocument: {
                index: 'drive.google.com/file/d',
                id: function (url) {
                    var m = url.match(/^.+drive.google.com\/file\/d\/(.+)\//);
                    if (m !== null) {
                        return m[1];
                    }
                    return null;
                },
                src: 'https://drive.google.com/file/d/%id%/preview'
            }
        }
    }
}
function panel_header_clicked(event) {
    event.stopImmediatePropagation();
    $(".floating-item").magnificPopup(magnificPopupConfig);
    $(".infosession-item").parent().parent().addClass("floating-item-css")
    chat.add_dummy_line();
    panel_clicked = "key-" + event.currentTarget.className.split('component-key-')[1]
    panel_components.forEach(function (c, i){
        collapsed = true;
        if (c === panel_clicked) {return;}
        component = formio.getComponent(c)
        if (component) {component.collapsed = collapsed};
    });
    $('.formio-component-panel').on('click', panel_header_clicked);
}

