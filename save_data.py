import datetime
import os
import shutil
import socket
from collections import OrderedDict

import requests
from bottle import default_app
from bottle import get
from bottle import request, response
from bottle import run
from bottle import static_file
from bottle import view, route
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from lib.docx import Document
from s.customize import Customize

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

true_socket = socket.socket


def make_bound_socket(source_ip):
    def bound_socket(*a, **k):
        sock = true_socket(*a, **k)
        sock.bind((source_ip, 0))
        return sock

    return bound_socket


timeout = 300
socket.setdefaulttimeout(timeout)
print("My external IP is: %s" % requests.get('http://httpbin.org/ip').content)

ROOT_PATH = os.path.dirname(__file__)


@route("/s/<filepath:path>")
def serve_s(filepath):
    return static_file(filepath, root="./s")


@get("/Sample")
@view("view/Sample")
def parameters():
    return {"title": "Adobe Analytics Parameter"}


@route("/save_data/", method="POST")
def save_data():
    response.headers['Content-Type'] = 'application/json'
    import json
    customize = Customize()
    try:
        try:
            data = request.json
        except ValueError:
            data = request.forms
            if data is None:
                default_app[0].log("input data is None", "error")
                raise ValueError
        if "ar" in data["filename"]:
            language = "ar"
        else:
            language = "no_ar"
        filedir = os.path.join(os.path.dirname(__file__), "s", "data", data["filename"] + ".html")
        f = open(filedir, 'w', encoding="utf-8")
        f.write(data["data"])
        f.close()
        back_up_dir = os.path.join(os.path.dirname(__file__), "s", "data_backup", data["filename"] + "_" + datetime.datetime.today().strftime(
            "%Y%m%d%H%M%S") + ".html")
        html_data = customize.modify_html(data["data"], language)
        back_up = open(back_up_dir, 'w', encoding="utf-8")
        back_up.write(html_data)
        back_up.close()

        soup = BeautifulSoup(data["data"], "lxml")
        document = Document()
        for i in soup.body.contents:
            if i.name == "h2":
                p = document.add_paragraph(style="Title")
                customize.document_style(language, p, i.string)
            elif i.name == "h3":
                p = document.add_paragraph(style="Heading 1")
                customize.document_style(language, p, i.string)
            elif i.name == "h4":
                p = document.add_paragraph(style="Heading 2")
                customize.document_style(language, p, i.string)
            elif i.name == "p":
                p = document.add_paragraph()
                for j in i.contents:
                    if j.name == "br":
                        p.add_run().add_break()
                    else:
                        customize.document_style(language, p, j.string, j.name)
            elif i.name == "ul":
                for li in i.contents:
                    p = document.add_paragraph(style="List Bullet")
                    for j in li.contents:
                        customize.document_style(language, p, j.string, j.name)
        file_word = os.path.join(os.path.dirname(__file__), "s", "data", data["filename"] + ".docx")
        file_word_backup = os.path.join(os.path.dirname(__file__), "s", "data_backup", data["filename"] + "_" + datetime.datetime.today().strftime(
            "%Y%m%d%H%M%S") + ".docx")
        document.save(file_word)
        shutil.copyfile(file_word, file_word_backup)

        json_result = OrderedDict()
        if "ar" in data["filename"]:
            json_result["rtl"] = True
        else:
            json_result["rtl"] = False
        json_section_result = OrderedDict()
        json_page_content = []
        for i in soup.body.contents:
            if i.name == "h3":
                if json_section_result:
                    if "content" not in json_section_result.keys():
                        json_section_result["full_text"] = True
                    json_page_content.append(json_section_result)
                    json_section_result = OrderedDict()
                json_section_result["heading"] = customize.html_escaped(i.string)
            elif i.name == "p":
                if "<u>" in str(i):
                    for j in i.contents:
                        if j.name == "u":
                            json_section_result["subheading"] = customize.html_escaped(j.string)
                else:
                    if "content" in json_section_result.keys():
                            json_section_result["content"] = json_section_result["content"] + customize.html_escaped(i.prettify(formatter="html"))
                    else:
                        json_section_result["content"] = customize.html_escaped(i.prettify(formatter="html"))
            elif i.name == "ul":
                if "content" in json_section_result.keys():
                    json_section_result["content"] = json_section_result["content"] + customize.html_escaped(i.prettify(formatter="html"))
                else:
                    json_section_result["content"] = customize.html_escaped(i.prettify(formatter="html"))
            elif i.name == "h4":
                if "content" in json_section_result.keys():
                    json_section_result["content"] = json_section_result["content"] + customize.html_escaped(i.prettify(formatter="html")).replace("<h4>", "<h3>").replace("</h4>", "</h3>")
                else:
                    json_section_result["content"] = customize.html_escaped(i.prettify(formatter="html")).replace("<h4>", "<h3>").replace("</h4>", "</h3>")
        json_page_content.append(json_section_result)
        json_result["page_content"] = json_page_content
        file_json = os.path.join(os.path.dirname(__file__), "s", "data_backup", data["filename"] + "_" + datetime.datetime.today().strftime(
            "%Y%m%d%H%M%S") + ".json")
        f = open(file_json, 'w', encoding="utf-8")
        json_data = json.dumps(json_result, ensure_ascii=False, indent=2)
        f.write(json_data)
        f.close()

    # except KeyError:
    #     return json.dumps({'code': 400, 'message': 'Bad Request, required field is missing.'})
    except ValueError:
        return json.dumps({'code': 400, 'message': "Can't save content, please try again."})
    # except IndexError:
    #     return json.dumps({'code': 400, 'message': 'index error.'})
    response.status = 200
    return json.dumps({'code': 200, 'message': 'Save succeed.'})


app = default_app()
run(app=app, host='0.0.0.0', port=8002)
