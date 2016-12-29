#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Alex on 2016/12/28
# http://huaban.com/boards/15759013/?qq-pf-to=pcqq.group&ix8ifcer&max=745069813&limit=20&wfl=1
# http://huaban.com/boards/15759013/?qq-pf-to=pcqq.group&ix8ifces&max=184558005&limit=20&wfl=1
import logging
import logging.config
import json

from blinker import signal
import requests

from content_pars import pars
# from sheduler import save_task

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("huaban")

session = requests.Session()

pin_message = signal("pin")

nexturl = "http://huaban.com/boards/2874262/?ix8zyuca&max={max}&limit=20&wfl=1"


def get_headers():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5',
                            'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = [
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0', ]
    _headers = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[2]
    }
    return _headers


def get_html_content(url):
    content = session.get(url, headers=get_headers())
    logger.debug(content)
    if content.ok:
        return content.text
    else:
        logger.debug("not ok")
        logger.debug(content.text)


def get_pins(pars):
    return pars.get("pins")


def get_pins_count(pars):
    return pars.get("pin_count")


def get_last_pin(pins):
    try:
        return pins[:-1][0]
    except:
        return None


def next_page_url(last_pin, nexturl=nexturl):
    url = nexturl.format(max=last_pin.get("pin_id"))
    return url


# @pin_message.connect
def send_pin(pin):
    save_task.delay(pin)


# @pin_message.connect
def save_pin(pin):
    with open("pins.txt", "a") as f:
        f.write(json.dumps(pin) + "\n")


def main(url):
    url = url
    par = True
    logger.info("=========begin============")

    logger.info(par)
    logger.info(url)
    par = pars(get_html_content(url))
    pins_cont = get_pins_count(par)
    logger.debug(pins_cont)
    _get_pins_count = 0
    step = 20
    while _get_pins_count < pins_cont:
        pins = get_pins(par)
        last_pin = get_last_pin(pins)
        for pin in pins:
            logger.debug(pin)
            pin_message.send(pin)
        url = next_page_url(last_pin)
        get_html_content(url)
        _get_pins_count += step
    logger.info("=============finished===========")


# print content.text

if __name__ == '__main__':
    url = "http://huaban.com/boards/2874262/"

    # par = pars(get_html_content(url))
    # logger.debug(par)
    #
    # pins = get_pins(par)
    # logger.debug(pins)
    #
    # last_pin = get_last_pin(pins)
    # logger.debug(last_pin)
    #
    # next_url = next_page_url(last_pin)
    # logger.debug(next_url)
    #
    # for pin in pins:
    #     send_pin(pin)

    main(url)
