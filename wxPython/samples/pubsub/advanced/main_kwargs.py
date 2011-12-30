'''
Uses topic definition provider for kwargs messaging protocol. Compare with 
main_arg1.py which shows example using arg1 messaging protocol: 
kwargs protocol provides for message data self-documentation and more 
robustness (pubsub can determine if message data missing or unknown due 
to type, etc).

Experiment by changing arg1_topics.py and looking at the output tree 
in kwargs_topics_out.py.

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
'''

from pubsub import setupkwargs
from pubsub import pub

import notifhandle
import exchandle

import kwargs_topics

#***** actual application **********

print 'Using "kwargs" messaging protocol of pubsub v3'

try:
    print '------- init ----------'

    pub.importTopicTree( kwargs_topics )
    pub.setTopicUnspecifiedFatal()

    import kwargs_listeners
    import kwargs_senders as senders

    senders.init()
    print '-----------------------'
    senders.doSomething1()
    senders.doSomething2()

    print '------- done ----------'

    print 'Exporting topic tree to', kwargs_topics.__name__
    pub.exportTopicTree('kwargs_topics_out')

except Exception, exc:
    import traceback
    traceback.print_exc()
    print pub.exportTopicTree()

print '------ exiting --------'