from flask import render_template, request
from flask_login import login_required

from app import admin_required
from app.application import test as mtest
from . import test
from app.application import test as msettings


@test.route('/test', methods=['GET', 'POST'])
def test():
    ret = mtest.execute_test(request.args)
    return str(ret)
