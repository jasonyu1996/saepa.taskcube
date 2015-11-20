from ..exceptions import TaskValidationException


class UserNotRegisteredException(TaskValidationException):
    def __init__(self, user_name):
        self.user_name = user_name
    def getInfo():
        return Markup('你需要绑定账号：http://taskcube.hqythu.me/wechat/login/%s' % user_name)


class CommandNotFoundException(TaskValidationException):
    def getInfo():
        return '不知道您在说什么'


class AlreadyDoTodayException(TaskValidationException):
    def getInfo():
        return '您今天已经领取过该任务了'

class TimeNotMatchException(TaskValidationException):
    def getInfo():
        return '现在这个时间不能领取该任务'

