$(document).ready(function() {
     heatMapper();
     setup();
});

var glob_bridge_state = {
    file: 'default'
};

function heatMapper()
{
    $('.loop').each(function(index) {
        var opac = $(this).children('.weight').html();
        $(this).fadeTo('slow', opac);
   });
}

function setup()
{   
    $('.ircode a').click( function() {   
        $(this).parent().find("a").removeClass("ass").addClass("tinyass");
        $(this).removeClass("tinyass");
        $(this).addClass("ass");
     });
    $('.full').hide(function (){
        
     });
     $('.full').click(function() {
        $(this).hide("slow");
        $(this).parent().children('.brief').show("slow");
     });
     $('.brief').click(function() {
        $(this).hide("slow");
        $(this).parent().children('.full').show("slow");
     });
}

function loop(loop)
{
    $(".loop.selected").removeClass("selected");
    $(".loop#"+loop).addClass("selected");
    glob_bridge_state.loopID = loop;
    $.getJSON('/loop',glob_bridge_state, function(arg) {
        $('#main').html(arg.html);
        $('#heatContainer').html(arg.heat);
        setup();
    });
    
}

function expansion(loop, line, chunk)
{
    var requestVar = {
        file: glob_bridge_state.file,
        loopID: loop,
        lineNo: line,
        chunkNo: chunk
    };
    $.getJSON('/expansion', requestVar, function(arg) {
        $("#line"+line).html(arg.html);
        $('#expand th').click( function() {
            $(this).parent().parent().parent().parent().hide();
            restore(line);
        });
        $("#line"+line).show();
        var position = $("#line" + line).position();

        scroll(0,position.top-200);
    });
}

function restore(line)
{
    $('#source'+line+' .ircode a').removeClass("ass");
    $('#source'+line+' .ircode a').removeClass("tinyass");
}

function viewAsm(asmID,asmID2)
{   
    if ($("#"+asmID2).hasClass('plus'))
    {
        $("#"+asmID2).removeClass("plus");
        $("#"+asmID2).addClass("minus");
        $("#"+asmID2).html('-');
        $("#"+asmID).show();
    }
    else
    {
        $("#"+asmID2).removeClass("minus");
        $("#"+asmID2).addClass("plus");
        $("#"+asmID2).html('+');
        $("#"+asmID).hide();
    }
}

function selectDirectory(base64Dir)
{
    $('#main').hide();
    $('#loops').hide();
    $('#name').hide();
    args = {
      directory: base64Dir  
    };
    $.getJSON('/directory', args, function(arg) {
        $("#pathContainer").html(arg.html);
    });
}

function selectFile(base64File)
{   
    args = {
        file: base64File
    };
    glob_bridge_state['file'] = base64File;
    $.getJSON('/getFile', args, function(arg) {
        $('#pathContainer').html(arg.path);
        $('#bannerContainer').html(arg.select);
        $('#fileContainer').html(arg.file);
        setup();
        heatMapper();
    });
    

}

function gotoLine(line)
{
    var position = $("#source" + line).position();
    scroll(0,position.top);
}



