#coding: utf-8
import os
from readability import Document
from app.common.url import *
from html2text import HTML2Text 
from flask import current_app
import uuid
from bs4 import BeautifulSoup


def get_url_html(html, url):
    if html is not None:
        return html
    return open_url(url)


def get_main_html(html):
    doc = Document(html)
    return doc.summary()


def download_html_image(url, html, image_path):
    """ 下载html中的图片 """
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.select("img")
    for img in imgs:
        src = img['src'] if not url else full_url(url, img["src"])
        _, ext = os.path.splitext(src)
        filename = "/{0}/{1}{2}".format(image_path, uuid.uuid1().hex, ext)
        full_filename = "{0}{1}".format(current_app.root_path, filename)
        filename = "{0}{1}".format(current_app.config["UPLOADIMG_HOST"], filename)
        if not download_file(src, full_filename):
            img['src'] = src
        else:
            img['src'] = filename
    return unicode(soup)


def html2markdown(html, url, download_image, image_path):
    if not download_image:
        h = HTML2Text(baseurl = url, bodywidth = 0)
    else:
        html = download_html_image(url, html, image_path)
        h = HTML2Text(bodywidth = 0)
    md = h.handle(html)
    return md

