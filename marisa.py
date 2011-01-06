#!/usr/bin/env python
# coding: utf8

# Copyright 2011 Kunshan Wang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import httplib
import urllib
import datetime
import json

class Marisa(object):
    HOST = 'bbs.saraba1st.com'
    ADDR = 'http://bbs.saraba1st.com/2b/Sunyanzi/marisa/io.php'

    def __init__(self):
        self.conn = httplib.HTTPConnection(Marisa.HOST)

    def send_message(self, key, value):
        self.conn.request(
                "POST",
                Marisa.ADDR,
                urllib.urlencode({key : value}),
                {"Content-Type":"application/x-www-form-urlencoded;charset=utf-8"}
                )
        resp = self.conn.getresponse()
        msg = json.loads(resp.read())

        return msg

    def init(self, hour=None):
        if hour==None:
            hour = datetime.datetime.now().hour
        return self.send_message("init", hour)

    def text(self, message):
        return self.send_message("text", message)

    def breath(self):
        return self.send_message("breath", "")

    def close(self):
        self.conn.close()

if __name__=='__main__':
    import sys
    import threading

    def marisa_says(response):
        if 'addtext' in response and response['addtext'] is not None:
            print response['addtext']
        print u'白絲魔理沙：'+response['message']

    print u'正在建立和白絲魔理沙的连接 ...'
    print u'人...人家才不是因为喜欢魔理沙，才写做这个脚本的...'
    marisa = Marisa()

    resp = marisa.init()
    marisa_says(resp)

    try:
        while True:
            line = raw_input(u"You:")
            resp = marisa.text(line)
            marisa_says(resp)
    except EOFError:
        pass
    finally:
        marisa.close()

