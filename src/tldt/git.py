import os
import os.path
import logging

import sh

logger = logging.getLogger(__name__)


class Repo(object):
    def __init__(self, local):
        self.local = local
        self.git = sh.git.bake(_cwd=local)

    def checkout(self, head):
        self.git.checkout(head)

    def clone(self, remote):
        return self.git.clone(remote, self.local)

    def fetch(self, remote):
        return self.git.fetch(remote)

    def clone_or_update(self, remote):
        if not os.path.exists(self.local):
            os.mkdir(self.local)
        try:
            self.git.status()
        except sh.ErrorReturnCode_128:
            logging.warn("cloning %s in to %s", remote, self.local)
            self.clone(remote)
        else:
            logging.warn("fetching %s in to %s", remote, self.local)
            self.fetch(remote)
