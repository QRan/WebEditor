#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup


class Customize:

    def modify_html(self, html, language):
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find("title").string
        body_content = soup.body
        body_content.find("h3").decompose()
        body_content.find("p").decompose()
        content = self.html_escaped(body_content.prettify(formatter="html")).replace("<body>", "").replace("</body>", "").\
            replace("<u>", "").replace("</u>", "").replace("&ndash;", "&#8211;").replace("„", "&#8222;")
        header = "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' " \
                 "'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>" \
                 "<html xmlns='http://www.w3.org/1999/xhtml'>" \
                 "<head>" \
                 "<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />" \
                 "<title>{title}</title>" \
                 "<style type='text/css' media='all'>" \
                 "<!--" \
                 "@import url('/ps3-eula/css/style.css');" \
                 "-->" \
                 "{ar}" \
                 "</style>" \
                 "</head>" \
                 "<body>" \
                 "<div id='container'>" \
                 "<div id='main'>"
        footer = "<!--PS3_ND_start-->" \
                 "<div id='prev'>" \
                 "<p><a href='javascript:window.history.back();'>Document selection</a></p>" \
                 "<p><a href='http://www.scei.co.jp/legal/'>Country / Region selection</a></p>" \
                 "</div>" \
                 "<!--PS3_ND_end-->" \
                 "<div id='copyright'></div></div></div></body></html>"
        header = header.replace("{title}", title)
        if language == "ar":
            header = header.replace("{ar}", "body{direction:rtl;}")
            content = content.replace('<body dir=&quot;rtl&quot;>', '')
        else:
            header = header.replace("{ar}", "")
        html_modified = header + content + footer
        return html_modified

    def html_escaped(self, data):
        data = data.replace("\"", "&quot;").replace("'", "&#39;").replace("<br/>", "<br />")
        data = re.sub("\n +", "", data).replace("\n", "")
        return data

    def document_style(self, lang, p, text, other_style=""):
        if lang == "ar":
            paragraph_format = p.paragraph_format
            paragraph_format.bidi = True
            if re.findall(r'[a-z]', text, re.I):
                text_en_all = re.findall(r'[htps?:/]*[a-z0-9 \/\.\#\-\®\™]+', text, re.I)
                for text_en in text_en_all:
                    if re.findall(r'[a-z]', text_en, re.I):
                        text = text.replace(text_en, "\u200e" + text_en + "\u200e")
                text_all = text.split("\u200e")
                for t in text_all:
                    if re.findall(r'[a-z]', t, re.I):
                        font = p.add_run(t).font
                        if other_style == "strong":
                            font.bold = True
                        elif other_style == "u":
                            font.underline = True
                    else:
                        font = p.add_run(t).font
                        font.rtl = True
                        if other_style == "strong":
                            font.bold = True
                        elif other_style == "u":
                            font.underline = True
            else:
                font = p.add_run(text).font
                font.rtl = True
                if other_style == "strong":
                    font.bold = True
                elif other_style == "u":
                    font.underline = True
        else:
            font = p.add_run(text).font
            if other_style == "strong":
                font.bold = True
            elif other_style == "u":
                font.underline = True
