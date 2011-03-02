from fabric.api import local
import os

DJANGROVE_DIR = os.path.abspath('.')

#this fabfile is a first-pass at making something we can use to start working.
#apps with develop branches.

ACTIVE_APPS = ["datadict"]

APP_REPOS = {'datadict': 'git@github.com:mangroveorg/datadict.git'}

def git_pull_all():
    """
    Clones/Pulls the develop branch of the mangrove subprojects
    necessary to get djangrove running.
    """
    for app_name in ACTIVE_APPS:
        if not os.path.exists( \
                os.path.join(DJANGROVE_DIR, app_name)):
            local("git clone -b develop %s" % APP_REPOS[app_name])
#        else:
#            local("cd %s && git pull origin develop" % app_name)

def setup_project():
    """
    run this the first time you load this project.
    """
    if not os.path.exists(os.path.join(DJANGROVE_DIR, "local_settings.py")):
        local("cp example_files/local_settings.py .")
    git_pull_all()