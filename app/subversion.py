# SubversionSyncr - 0.0.2
#
# Author:  Maxime Haineault <haineault@gmail.com>
# License: MIT License ~ http://www.opensource.org/licenses/mit-license.php
# Documentation: http://code.google.com/p/django-syncr/wiki/SyncrSubversion

from datetime import datetime
from syncr.subversion.models import Revision
from django.conf import settings

# This apps depends on pysvn (http://pysvn.tigris.org/)
# Debian based distros: sudo apt-get install pysvn
import pysvn, cjson


def get_login( realm, username, may_save ):
    return True, 'username', 'password', True

SVN_SYNCS = (
    {'url': 'http://django-syncr.googlecode.com/svn/trunk/'},
#   {'url': 'https://django-syncr.googlecode.com/svn/trunk/', 'username': 'bob', 'password': 'god'},
)

SVN_REVISION_START = getattr(settings, 'SVN_REVISION_START', pysvn.Revision(pysvn.opt_revision_kind.head))
SVN_REVISION_END = getattr(settings, 'SVN_REVISION_END', pysvn.Revision(pysvn.opt_revision_kind.number, 0))
SVN_DISCOVER_CHANGED_PATHS = getattr(settings, 'SVN_DISCOVER_CHANGED_PATHS', True)
SVN_STRICT_NODE_HISTORY = getattr(settings, 'SVN_STRICT_NODE_HISTORY', True)
SVN_LIMIT = getattr(settings, 'SVN_LIMIT', 1000)
SVN_PEG_REVISION = getattr(settings, 'SVN_LIMIT', pysvn.Revision(pysvn.opt_revision_kind.unspecified))
SVN_INCLUDE_MERGED_REVISIONS = getattr(settings, 'SVN_INCLUDE_MERGED_REVISIONS', False)


def getoption(repos, key, default=False):
    if key in repos:
        return repos[key]
    else:
        return default

def get_changed_paths_json(paths, o=[]):
    for path in paths:
        o.append({
            'action': path.data['action'],
            'path': path.data['path'],
            'copyfrom_path': path.data['copyfrom_path'] or 'false',
            'copyfrom_revision': path.data['copyfrom_revision'] and path.data['copyfrom_revision'].number or 'false',
        })
    return cjson.encode(o)

class SubversionSyncr:
    """
    SubversionSyncr objects sync subversion revisions log with the Django backend.
    """

    def syncRevisions(self):
        """
        Synchronize Subversion revisions from a SVN server
        """

        for repos in SVN_SYNCS:
            print '[syncr:subversion] synchronizing: %s' % repos['url']

            
            client = pysvn.Client()

            if 'get_login' in repos:
                client.callback_get_login = repos['get_login']

            logs = client.log(repos['url'],
                revision_start=getoption(repos, 'start', SVN_REVISION_START),
                revision_end=getoption(repos, 'end', SVN_REVISION_END),
                discover_changed_paths=getoption(repos, 'discover_changed_paths', SVN_DISCOVER_CHANGED_PATHS),
                strict_node_history=getoption(repos, 'strict_node_history', SVN_STRICT_NODE_HISTORY),
                limit=getoption(repos, 'limit', SVN_LIMIT),
                peg_revision=getoption(repos, 'peg_revision', SVN_PEG_REVISION),
                include_merged_revisions=getoption(repos, 'include_merged_revisions', SVN_INCLUDE_MERGED_REVISIONS))

            count = 0
            for log in logs:
                rev = Revision(
                        svnPath = u'%s' % repos['url'],
                        date = datetime.fromtimestamp(log.data['date']),
                        has_children = log.data['has_children'],
                        message = log.data['message'],
                        revision = log.data['revision'].number,
                        revision_kind = str(log.data['revision'].kind),
                        )
                if 'changed_paths' in log.data:
                    rev.changed_paths = u'%s' % get_changed_paths_json(log.data['changed_paths'])
                if 'author' in log.data:
                    rev.author = u'%s' % log.data['author']

                try:
                    rev.save()
                    count = count + 1
                except Exception, e:
                    print 'Sync Error: %s' % (e)

            print '[syncr:subversion] synchronized %s revision(s)' % count
