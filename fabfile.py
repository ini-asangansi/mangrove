from fabric.api import local, cd
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
    dirty_repos = []
    for app_name in ACTIVE_APPS:
        if not os.path.exists( \
                os.path.join(DJANGROVE_DIR, app_name)):
            local("git clone -b develop %s" % APP_REPOS[app_name])
    else:
        with cd(app_name):
            #a kinda dirty way of checking if there are local changes...
            status = local("git status | grep -qF 'working directory clean' || echo 'dirty'")            
            if status=="dirty":
                dirty_repos.append(app_name)
            else:
                print "Pulling most recent changes %s" % app_name
                print local("git pull origin develop")
    if len(dirty_repos) > 0:
        dirty_repo_list = ", ".join(dirty_repos)
        raise Exception("Local changes on %d repository/repositories:\n%s" % \
                            (len(dirty_repos), dirty_repo_list))

def setup_project():
    """
    run this the first time you load this project.
    """
    if not os.path.exists(os.path.join(DJANGROVE_DIR, "local_settings.py")):
        local("cp example_files/local_settings.py .")
    git_pull_all()