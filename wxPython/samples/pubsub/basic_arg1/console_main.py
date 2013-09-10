'''

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

from pubsub import setuparg1

import console_senders as senders
import console_listeners


def run():
    print 'Using "arg1" messaging protocol of pubsub v3'

    senders.doSomething1()
    senders.doSomething2()


if __name__ == '__main__':
    run()
