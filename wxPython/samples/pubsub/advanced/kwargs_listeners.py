'''

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
'''

from pubsub import pub

# ------------ create some listeners --------------

class Listener:
    def onTopic11(self, msg, msg2, extra=None):
        print 'Method Listener.onTopic11 received: ', `msg`, `msg2`, `extra`

    def onTopic1(self, msg, topic=pub.AUTO_TOPIC):
        info = 'Method Listener.onTopic1 received "%s" message: %s'
        print info % (topic.getName(), `msg`)

    def __call__(self, **kwargs):
        print 'Listener instance received: ', kwargs

listenerObj = Listener()


def listenerFn(msg, msg2, extra=None):
    print 'Function listenerFn received: ', `msg`, `msg2`, `extra`

# ------------ subscribe listeners ------------------

pub.subscribe(listenerObj, pub.ALL_TOPICS) # via its __call__

pub.subscribe(listenerFn, 'topic_1.subtopic_11')
pub.subscribe(listenerObj.onTopic11, 'topic_1.subtopic_11')

pub.subscribe(listenerObj.onTopic1, 'topic_1')

