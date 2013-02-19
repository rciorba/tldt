import sh


class Repo(object):
    def __init__(self, local):
        self.git = sh.git.bake(_cwd=local)

    def checkout(self, head):
        self.git.checkout(head)

    def clone(self, remote):
        return self.git.clone(remote)

    def fetch(self, remote):
        return self.git.fetch(remote)
