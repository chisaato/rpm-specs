import os
from os import path

include('defaults.cfg')
config_opts['root'] = 'fedora-{{ releasever }}-{{ target_arch }}'

config_opts['description'] = 'Fedora {{ releasever }} 国内镜像版'
# fedora 31+ isn't mirrored, we need to run from koji
config_opts['mirrored'] = config_opts['target_arch'] != 'i686'

config_opts['chroot_setup_cmd'] = 'install @{% if mirrored %}buildsys-{% endif %}build'

# only useful for --resultdir variable subst
config_opts['dist'] = 'fc{{ releasever }}'
config_opts['extra_chroot_dirs'] = ['/run/lock', ]
config_opts['package_manager'] = 'dnf'
config_opts['bootstrap_image'] = 'registry.fedoraproject.org/fedora:{{ releasever }}'

conf_dir = os.getcwd()
# 这里挂载镜像列表
config_opts['plugin_conf']['bind_mount_opts']['dirs'].append(
    (path.join(conf_dir, "..", "mock-config", "mirrorlist"), '/etc/dnf/mirrorlist'))
# (path.join(conf_dir, "mock-config", "mirrorlist"), '/etc/dnf/mirrorlist'))


config_opts['dnf.conf'] = """
[main]
keepcache=1
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
install_weak_deps=0
metadata_expire=0
best=1
# 对于国内使用,最好关掉 zck
zchunk=False
# 可能有效,对于挑选一个单线程速度快的
fastestmirror=0
module_platform_id=platform:f{{ releasever }}
protected_packages=
user_agent={{ user_agent }}

# repos

[local]
name=local
baseurl=https://kojipkgs.fedoraproject.org/repos/f{{ releasever }}-build/latest/$basearch/
cost=2000
enabled={{ not mirrored }}
skip_if_unavailable=False

{% if mirrored %}
# 原版仓库

[fedora]
name=Fedora $releasever - $basearch
mirrorlist=file:///etc/dnf/mirrorlist/fedora.mirrorlist
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-debuginfo]
name=Fedora $releasever - $basearch - Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-source]
name=Fedora $releasever - Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

# 更新仓库

[updates]
name=Fedora $releasever - $basearch - Updates
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates.mirrorlist
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-debuginfo]
name=Fedora $releasever - $basearch - Updates - Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-source]
name=Fedora $releasever - Updates Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

# 测试更新仓库

[updates-testing]
name=Fedora $releasever - $basearch - Test Updates
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-testing-debuginfo]
name=Fedora $releasever - $basearch - Test Updates Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-testing-source]
name=Fedora $releasever - Test Updates Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

# Modular 仓库

[fedora-modular]
name=Fedora Modular $releasever - $basearch
mirrorlist=file:///etc/dnf/mirrorlist/fedora-modular.mirrorlist
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-modular-debuginfo]
name=Fedora Modular $releasever - $basearch - Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-modular-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-modular-source]
name=Fedora Modular $releasever - Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-modular-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

# Modular 更新仓库

[updates-modular]
name=Fedora Modular $releasever - $basearch - Updates
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-modular.mirrorlist
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-modular-debuginfo]
name=Fedora Modular $releasever - $basearch - Updates - Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-modular-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-modular-source]
name=Fedora Modular $releasever - Updates Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-modular-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

# Modular 更新测试仓库

[updates-testing-modular]
name=Fedora Modular $releasever - $basearch - Test Updates
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing-modular.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-testing-modular-debuginfo]
name=Fedora Modular $releasever - $basearch - Test Updates Debug
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing-modular-debuginfo.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[updates-testing-modular-source]
name=Fedora Modular $releasever - Test Updates Source
mirrorlist=file:///etc/dnf/mirrorlist/fedora-updates-testing-modular-source.mirrorlist
enabled=0
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

{% endif %}
"""
