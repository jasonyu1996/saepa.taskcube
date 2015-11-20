from flask import request
from flask import render_template
from flask import redirect
from flask import Markup
from . import main
from .forms import UserForm
from .. import db
from ..models import User
from .util import check
from .util import xmlparse
from . import handler
from .exceptions import *


@main.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@main.route('/wechat', methods=['GET'])
def wechat_check():
    check_result = check.check_signature(
        request.args.get('signature', ''),
        request.args.get('timestamp', ''),
        request.args.get('nonce', ''),
        request.args.get('echostr', '')
    )
    if check_result:
        return request.args.get('echostr', '')
    else:
        return ''


@main.route('/wechat', methods=['POST'])
def wechat_response():
    message = xmlparse.get_message_by_xml(request.data)
    try:
        reply = handler.handler(message)
    except UserNotRegisteredException:
        reply = handler.construct_reply_message(
            message,
            Markup('你需要绑定账号：http://taskcube.hqythu.me/wechat/login/%s' %
                   message.get('FromUserName', ''))
        )
    except CommandNotFoundException:
        reply = handler.construct_reply_message(
            message,
            '不知道您在说什么'
        )
    return render_template('reply_text.xml', msg=reply)


@main.route('/wechat/success', methods=['GET'])
def success():
    return render_template('success.html')


@main.route('/wechat/login/<openid>', methods=['GET', 'POST'])
def login(openid):
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            openid=openid,
            credits=0
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/wechat/success')
    return render_template('login.html', form=form)
