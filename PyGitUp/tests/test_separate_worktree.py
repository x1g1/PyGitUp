# System imports
import os
from os.path import join

from git import *
from git.util import cygpath
from nose.tools import *

from PyGitUp.tests import basepath, init_master, update_file

test_name = 'worktree'
repo_path = join(basepath, test_name + os.sep)
worktree_dir = '{}_worktree'.format(test_name)
worktree_path = join(basepath, worktree_dir)


def setup():
    master_path, master = init_master(test_name)

    # Prepare master repo
    master.git.checkout(b=test_name)

    # Clone to test repo
    path = join(basepath, test_name)

    master.clone(path, b=test_name)

    # Create work tree
    clone = Repo(path, odbt=GitCmdObjectDB)
    clone.git.worktree('add', '../' + worktree_dir)

    # repo = Repo(worktree_path, odbt=GitCmdObjectDB)
    # assert repo.working_dir == worktree_path

    # Modify file in master
    update_file(master, test_name)


def test_separate_worktree():
    """ Run 'git up' with separate work tree """
    os.chdir(worktree_path)

    from PyGitUp.gitup import GitUp
    gitup = GitUp(testing=True)
    gitup.run()

    assert_equal(len(gitup.states), 1)
    assert_equal(gitup.states[0], 'fast-forwarding')
