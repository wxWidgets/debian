'''

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

from pubsub import pub
from pubsub.utils.notification import useNotifyByWriteFile, IgnoreNotificationsMixin


# create one special notification handler that ignores all except
# one type of notification
class MyPubsubNotifHandler(IgnoreNotificationsMixin):

    def notifySubscribe(self, pubListener, topicObj, newSub):
        newSubMsg = ''
        if not newSub:
            newSubMsg = ' was already'
        msg = 'MyPubsubNotifHandler: listener %s%s subscribed to %s'
        print msg % (pubListener.name(), newSubMsg, topicObj.getName())


pub.addNotificationHandler( MyPubsubNotifHandler() )


# print all notifications to stdout
import sys
useNotifyByWriteFile(sys.stdout, prefix='NotifyByWriteFile:')
