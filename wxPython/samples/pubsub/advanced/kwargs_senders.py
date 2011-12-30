'''

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

from pubsub import pub


def init():
    '''Do something that changes topic tree so exportTopicTree interesting'''
    
    def proto(msg, arg1=None): pass
    topic = pub.getOrCreateTopic('topic_2.subtopic_21', proto)
    topic.setDescription( 'description for subtopic 21')


def doSomething1():
    pub.sendMessage('topic_1.subtopic_11', msg='message for subtopic 11', msg2='other message', extra=123)


def doSomething2():
    pub.sendMessage('topic_1', msg='message for topic 1')
    pub.sendMessage('topic_2.subtopic_21', msg='message for subtopic 2')


