
var glob_bridge_state = {
    'asm': false,
    'op': true,
};

function show_loop(name, path)
{
    $("#loop-" + glob_bridge_state.name).removeClass("selected");
    $("#loop-" + name).addClass("selected");
    $("#title-text").html($("#loop-" + name).attr('name'));
    $("#title").show();
    glob_bridge_state.name = name;
    if (path) {
        glob_bridge_state.path = path;
    } else {
        delete glob_bridge_state.path;
    }
    $.getJSON('/loop', glob_bridge_state, function(arg) {
        $('#main').html(arg.html).ready(function() {
            var scrollto;
            if (arg.scrollto == 0) {
                scrollto = 0;
            } else {
                scrollto = arg.scrollto - 1;
            }
            $.scrollTo($('#line-' + scrollto), 200, {axis:'y'});
        });
        $('#callstack').html('')
        for (var index in arg.callstack) {
            var elem = arg.callstack[index];
            $('#callstack').append('<div><a href="/" onClick="show_loop(' + name + ', \'' + elem[0] + '\'); return false">' + elem[1] + "</a></div>");
        }
        if (!glob_bridge_state.asm) {
            $(".asm").hide();
        }
    });
}

function document_ready()
{
    var l = window.location.search.substr(1).split('&');
    for (var s in l) {
        var l2 = l[s].split('=', 2);
        var name = l2[0];
        var val = l2[1];
        if (name == 'show_loop') {
            show_loop(val);
        }
    }
    $("#inp-bar").focus();
    $("#inp-bar").bind("click keyup", function() {
        var value = $("#inp-bar")[0].value;
        $(".loopitem").each(function (i, l) {
            glob = l;
            if (l.getAttribute('name').search(value) != -1) {
                $(l).show();
            } else {
                $(l).hide();
            }
        });
    });
}

function replace_from(elem, bridge_id)
{
    if (glob_bridge_state['loop-' + bridge_id]) {
        delete glob_bridge_state['loop-' + bridge_id];
    } else {
        glob_bridge_state['loop-' + bridge_id] = true;
    }
    $.getJSON('/loop', glob_bridge_state, function(res) {
        $('#main').html(res.html).ready(function() {
            for (var v in glob_bridge_state) {
                if (v.search('loop-') != -1) {
                    if (glob_bridge_state[v]) {
                        $('#' + v).next().html('&lt;&lt;hide bridge');
                    } else {
                        $('#' + v).next().html('&gt;&gt;show bridge');
                    }
                }
            }
            if (!glob_bridge_state.asm) {
                $(".asm").hide();
            }
            $.scrollTo($("#loop-" + bridge_id), {axis:'y'});
        });
    });
}

function asmtoggle()
{
    var e = $("#asmtoggler");
    var e2 = $(".asm");
    if (e.html().search("Show") != -1) {
        glob_bridge_state.asm = true;
        e.html("Hide assembler");
        e2.show();
    } else {
        glob_bridge_state.asm = false;
        e.html("Show assembler");
        e2.hide();
    }
}

function highlight_var(elem)
{
    $('.' + elem.className).addClass("variable_highlight");
}

function disable_var(elem)
{
    $(".variable_highlight").removeClass("variable_highlight");
}
