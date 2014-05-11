from fabric.api import *
from fabric.contrib import files

def vagrant():
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2201']
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]

def uname():
    run('uname -a')

def cmd_exists(cmd):
  return files.exists("/usr/bin/%s" % cmd)

def apt(cmdline):
  if not cmd_exists("aptitude"):
    sudo("apt-get -y install aptitude")
  sudo("aptitude %s" % cmdline)

def apt_install(packages):
  apt("-y install %s" % packages)

def apt_update():
  apt("update")
  
def apt_upgrade():
  apt_update()
  apt("-y safe-upgrade")
  
def bootstrap():
    apt_update()
    apt_install('build-essential git-core vim apache2 a2enmod rewrite')
    apt_install('build-essential git git-core')
    apt_install('python2.7-dev')
    apt_install('python-pip')
    apt_install('libmysqlclient-dev')
    apt_install('mysql-server')
    run('mysqladmin -u root password root')
    