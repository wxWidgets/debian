'''

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

from pubsub import pub


def init():
    '''Do something that changes topic tree so exportTopicTree interesting'''
    
    topic = pub.getOrCreateTopic('topic_2.subtopic_21')
    topic.setDescription( 'description for subtopic 21')


def doSomething1():
    pub.sendMessage('topic_1.subtopic_11', ('message for subtopic 11', 'other message', 123))


def doSomething2():
    pub.sendMessage('topic_1', 'message for topic 1')
    pub.sendMessage('topic_2.subtopic_21', 'message for subtopic 2')


