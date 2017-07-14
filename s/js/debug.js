function loadDoc(datafile) {
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }
    else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET", datafile, false);
    xmlhttp.send();
    return xmlhttp.responseText;
}

function save(){
    // Get the editor data.
    var filename = $("#selectfile").val(),
        data = CKEDITOR.instances.editor.getData(),
        jsondata = {
        "data": data,
        "filename": filename
        };
    $.ajax({
    url: "/save_data/",
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(jsondata),
    success: function(result){
            $("#output").html(result["message"]);
        }
    });
}

function download(){
    var filename = $("#selectfile").val(),
        file_link = "/s/data/" + filename + ".docx"
    window.location.href = file_link;
}

function changefile(){
    var filename = $("#selectfile").val(),
        lang = filename.slice(-2),
        filedir = "/s/data/e_privacy_lang.html",
        editor = CKEDITOR.instances["editor"];
    if (editor) {editor.destroy(true);};
    if (lang == "ar"){
        CKEDITOR.replace('editor', {
            width: '70%',
            height: 500,
            fullPage: true,
            contentsLangDirection: 'rtl',
        })
    }
    else {
        CKEDITOR.replace('editor', {
            width: '70%',
            height: 500,
            fullPage: true,
            contentsLangDirection: 'ltr',
        });
    };
    // Update the text area.
    CKEDITOR.instances.editor.setData(loadDoc(filedir.replace(/lang/, lang)));
    $("#output").html("")
}