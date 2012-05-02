var glob_bridge_state = {
    file: 'default'
};

function loop(loop)
{
    $(".loop.selected").removeClass("selected");
    $(".loop#"+loop).addClass("selected");
    glob_bridge_state.loopID = loop;
    $.getJSON('/loop',glob_bridge_state, function(arg) {
        $('#main').html(arg.html);
        $('#heatContainer').html(arg.heat);
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
        $("#line"+line).show();
    });
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
    });

}

function gotoLine(line)
{
    $.scrollTo($("#source-" + line), {axis:'y'});
}

