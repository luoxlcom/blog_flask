# -*- coding: utf-8 -*-
# @Author: phithon
# @Date:   2016-10-19 16:35:35

from app import create_app

if __name == '__main__':
    app = create_app('development')
    app.run()