#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sessions2trash.py

Run this script in a web2py environment shell e.g. python web2py.py -S app
If models are loaded (-M option) auth.settings.expiration is assumed
for sessions without an expiration. If models are not loaded, sessions older
than 60 minutes are removed. Use the --expiration option to override these
values.

Typical usage:

    # Delete expired sessions every 5 minutes
    nohup python web2py.py -S app -M -R scripts/sessions2trash.py &

    # Delete sessions older than 60 minutes regardless of expiration,
    # with verbose output, then exit.
    python web2py.py -S app -M -R scripts/sessions2trash.py -A -o -x 3600 -f -v

    # Delete all sessions regardless of expiry and exit.
    python web2py.py -S app -M -R scripts/sessions2trash.py -A -o -x 0
"""

from gluon.storage import Storage
from optparse import OptionParser
import cPickle
import datetime
import os
import stat
import time

EXPIRATION_MINUTES = 60
SLEEP_MINUTES = 5
VERSION = 0.3


def main():
    """Main processing."""

    usage = '%prog [options]' + '\nVersion: %s' % VERSION
    parser = OptionParser(usage=usage)

    parser.add_option('-o', '--once',
        action='store_true', dest='once', default=False,
        help='Delete sessions, then exit.',
        )
    parser.add_option('-s', '--sleep',
        dest='sleep', default=SLEEP_MINUTES * 60, type="int",
        help='Number of seconds to sleep between executions. Default 300.',
        )
    parser.add_option('-x', '--expiration',
        dest='expiration', default=None, type="int",
        help='Expiration value for sessions without expiration (in seconds)',
        )
    parser.add_option('-f', '--force',
        action='store_true', dest='force', default=False,
        help=('Ignore session expiration. '
            'Force expiry based on -x option or auth.settings.expiration.')
        )
    parser.add_option('-v', '--verbose',
        action='store_true', dest='verbose', default=False,
        help='Print verbose output.',
        )

    (options, unused_args) = parser.parse_args()

    expiration = options.expiration
    if expiration is None:
        try:
            expiration = auth.settings.expiration
        except:
            expiration = EXPIRATION_MINUTES * 60

    while True:
        trash_session_files(expiration, options.force, options.verbose)

        if options.once:
            break
        else:
            time.sleep(options.sleep)


def trash_session_files(expiration, force=False, verbose=False):
    """
    Trashes expired session files.

    Arguments::
        expiration: integer, expiration value to use for sessions without one.
        force: If True, ignores session expiration and use value of
                expiration argument.
        verbose: If True, print names of sessions trashed.
    """
    now = datetime.datetime.now()

    path = os.path.join(request.folder, 'sessions')
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        last_visit = datetime.datetime.fromtimestamp(
                os.stat(filename)[stat.ST_MTIME])

        if expiration > 0:
            try:
                f = open(filename, 'rb+')
                try:
                    session = Storage()
                    session.update(cPickle.load(f))
                finally:
                    f.close()

                if session.auth:
                    if session.auth.expiration and not force:
                        expiration = session.auth.expiration
                    if session.auth.last_visit:
                        last_visit = session.auth.last_visit
            except:
                pass

        if expiration == 0 or \
                total_seconds(now - last_visit) > expiration:
            os.unlink(filename)
            if verbose:
                print('Session trashed: %s' % file)


def total_seconds(delta):
    """
    Adapted from Python 2.7's timedelta.total_seconds() method.

    Args:
        delta: datetime.timedelta instance.
    """
    return (delta.microseconds + (delta.seconds + (delta.days * 24 * 3600)) * \
            10 ** 6) / 10 ** 6

main()

