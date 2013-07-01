# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.home.simpletab import SimpleTab
from Products.XWFCore.XWFUtils import get_user
from Products.CustomUserFolder.interfaces import IGSUserInfo


class PolicyTab(SimpleTab):
    def __init__(self, group, request, view, manager):
        SimpleTab.__init__(self, group, request, view, manager)
        self.manager = manager

    @property
    def participationCoach(self):
        uid = getattr(self.context, 'ptn_coach_id', '')

        user = get_user(self.context, uid)

        userInfo = None
        if user:
            userInfo = IGSUserInfo(user)

        return userInfo

    @Lazy
    def mailingList(self):
        retval = createObject('groupserver.MailingListInfo', self.context)
        assert retval
        return retval

    @property
    def postsPerDayLimit(self):
        groupList = self.mailingList.mlist
        senderlimit = groupList.getProperty('senderlimit', 512)
        senderinterval = groupList.getProperty('senderinterval', 86400)

        # convert 'old' system to posts per second, then per day (rounded)
        postsPerSecond = float(senderlimit)/float(senderinterval)
        postsPerDay = int(postsPerSecond*86400)

        return postsPerDay
