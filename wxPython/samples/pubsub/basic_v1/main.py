'''
This example demonstrates how to use the arg1 messaging protocol, in the
original pubsub version 1.

There are several listeners created for three topics: topic1, topic2, and 
"everything". A couple of functions are created that send messages. 

The main constraints are:

- only the second argument in the sendMessage() can carry message 
  data; extra named (i.e. optional) parameters are possible
  but will never receive data via pubsub. To send more data,
  you would have to package it into a tuple or a class instance 
  and pass it as second argument. 
- all topics along a topic branch get the same data; this doesn't 
  make much sense in general since typically only subtopics need extra 
  data, the parent topics wouldn't know what to do with the extra 
  info. 
- listeners must be callable with one argument, no more and 
  no less. The argument name can be anything. 

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

from pubsub import setupv1
from pubsub import Publisher as pub

# ------------ create some listeners --------------

def listener1(msg, extra=None):
    print 'Function listener1 received', msg.data

class Listener:    
    def onTopic1(self, msg, extra=None):
        print 'Method Listener.onTopic1 received', `msg.data`
    def onTopic2(self, msg):
        print 'Method Listener.onTopic2 received', `msg.data`
    def __call__(self, msg):
        print 'Listener() received', `msg.data`

# ------------ register listeners ------------------

pub.subscribe(listener1, 'topic1')

listener2 = Listener()
pub.subscribe(listener2) # ALL topics!
pub.subscribe(listener2.onTopic1, 'topic1')
pub.subscribe(listener2.onTopic2, 'topic2')

# ------------ create a couple of senders --------------

def doSomething1():
    print '--- SENDING topic1 message ---'
    pub.sendMessage('topic1', 'message1')
    print '---- SENT topic1 message ----'
    
def doSomething2():
    print '--- SENDING topic2 message ---'
    pub.sendMessage('topic2', 123)
    print '---- SENT topic2 message ----'
    
# --------- define the main part of application --------

def run():
    '''Loop until we get a quit message or user breaks.'''
    doSomething1()
    doSomething2()
    print 'done'


if __name__ == '__main__':
    run()
    