<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <title>A Simple Page with CKEditor</title>
        <link rel="stylesheet" type="text/css" href="s/css/style.css?v20170622" />
        <!-- Make sure the path to CKEditor is correct. -->
        <script src="/s/ckeditor/ckeditor.js?v=20170704"></script>
        <script src="/s/js/jquery.min.js"></script>
        <script src="/s/ckeditor/adapters/jquery.js"></script>
        <script src="/s/js/debug.js?v=20170703"></script>
    </head>
    <body>
        <p>Please select the file you want to change</p>
        <select title="selection" id="selectfile" onchange="changefile()">
            <option value="e_privacy_en">e_privacy_en</option>
            <option value="e_privacy_ar">e_privacy_ar</option>
        </select>
        <form>
            <textarea name="editor" id="editor" rows="10" cols="80">
            </textarea>
            <script>
                // Replace the <textarea id="editor"> with a CKEditor instance, using default configuration.
                CKEDITOR.replace('editor', {
                    width: '70%',
                    height: 500,
                    fullPage: true,
                    language: 'en',
                    allowedContent: true,
                });
                CKEDITOR.on( 'instanceReady', function( ev ) {
                    var writer = ev.editor.dataProcessor.writer,
                        dtd = CKEDITOR.dtd;
                    // Ends self-closing tags the HTML4 way, like <br />.
                    writer.selfClosingEnd = ' />';
                    ev.editor.dataProcessor.writer.setRules( 'br', {
                            indent : false,
                            breakBeforeOpen : false,
                            breakAfterOpen : false,
                            breakBeforeClose : false,
                            breakAfterClose : false
                    });
                    for ( var e in CKEDITOR.tools.extend( {}, dtd.$block) )
                    {
                        ev.editor.dataProcessor.writer.setRules( e, {
                            // Indicates that an element creates indentation on line breaks that it contains.
                            indent : false,
                            // Inserts a line break before a tag.
                            breakBeforeOpen : true,
                            // Inserts a line break after a tag.
                            breakAfterOpen : false,
                            // Inserts a line break before the closing tag.
                            breakBeforeClose : false,
                            // Inserts a line break after the closing tag.
                            breakAfterClose : false
                        });
                    };
                    for ( var e in CKEDITOR.tools.extend( {}, dtd.$listItem) )
                    {
                        ev.editor.dataProcessor.writer.setRules( e, {
                            indent : false,
                            breakBeforeOpen : false,
                            breakAfterOpen : false,
                            breakBeforeClose : false,
                            breakAfterClose : false
                        });
                    };
                });
                // Update the text area.
                CKEDITOR.instances.editor.setData(loadDoc('/s/data/e_privacy_en.html'));
            </script>
        </form>
        <button id="save" onclick="save()" type="button">Save</button>
        <button id="download" onclick="download()" type="button">Save as word file on local</button>
        <div id="output">
        </div>
    </body>
</html>