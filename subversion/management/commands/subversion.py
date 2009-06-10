import logging, pysvn
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from syncr.app.subversion import SubversionSyncr
from syncr.subversion.models import SubversionSync, Revision

logging.basicConfig(level=logging.DEBUG)

def test(blah):
    return 'yay %s' % blah

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
       #make_option('-d', '--dry-run', dest='dry_run', action='store_false',
       #            default=True, help='Sync but don\'t store anything in the database'),
    )
    help = 'Synchronize subversion repositories with Django'

    def handle(self, action='sync', **options):
        if action == 'sync':
            self.sync()
        elif action == 'reset':
            Revision.objects.all().delete()


    def sync(self):
        repo = {}
        svn  = SubversionSyncr()
        logging.info('Syncr.subversion: Sychronizing')

        # Use settings.py
        if hasattr(settings, 'SVN_SYNCS'):
            for sync in settings.SVN_SYNCS:
                c = svn.syncRevisions(**sync)
                logging.info('Syncr.subversion: Sychronized %s revisions' % c)
            
        # Use database to retreive settings
        else:
            for sync in SubversionSync.objects.all():
                kwargs = {
                    'url': sync.url,
                    'limit': sync.limit,
                    'discover_changed_paths': sync.discover_changed_paths,
                    'include_merged_rev': sync.include_merged_rev,
                    'strict_node_history': sync.strict_node_history,
                    }
                if getattr(sync, 'rev_start') != None:
                    kwargs['start'] = pysvn.Revision(pysvn.opt_revision_kind.number, int(sync.rev_start))
                else:
                    kwargs['start'] = pysvn.Revision(pysvn.opt_revision_kind.head)

                if getattr(sync, 'rev_end') != None:
                    kwargs['end'] = pysvn.Revision(pysvn.opt_revision_kind.number, int(sync.rev_end))

                if getattr(sync, 'peg_revision') != None:
                    kwargs['peg_revision'] = pysvn.Revision(pysvn.opt_revision_kind.number, int(sync.peg_revision))
                else:
                    kwargs['peg_revision'] = pysvn.Revision(pysvn.opt_revision_kind.unspecified)

                if hasattr(sync, 'username'):
                    kwargs['get_login'] = lambda: True, sync.username, sync.password, True

                c = svn.syncRevisions(**kwargs)
                logging.info('Syncr.subversion: Sychronized %s revisions' % c)
