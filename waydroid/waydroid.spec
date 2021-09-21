%global     forgeurl    https://github.com/waydroid/waydroid
%global     commit      15bbf62e43e8e2482aab809d24153fcbfc83a7bf
%forgemeta -i

Name:       waydroid
Version:    1
Release:    0.0%{?dist}
Summary:    Run Android in LXC

License:    GPLv3+
URL:        %{forgeurl}
Source:     %{forgesource}

BuildRequires:  python3
BuildRequires:  git

Requires:       python3-gbinder-python

# For SELinux
BuildRequires: selinux-policy-devel
Requires(post): policycoreutils
Requires(preun): policycoreutils
Requires(postun): policycoreutils

%description
Android™ application support
waydroid allows running a separate Android™ environment
confined to a LXC container.

%define waydroid_dir   %{name}-%{commit}

%prep
rm -rf %{waydroid_dir}
git clone --recurse-submodules %{forgeurl}.git %{waydroid_dir}
cd %{waydroid_dir}
git checkout %{commit}

%build
cd %{waydroid_dir}
# 没有构建

%install
cd %{waydroid_dir}
# 安装
install -dm755 %{buildroot}%{_libdir}/waydroid
install -dm755 %{buildroot}%{_datadir}/applications
install -dm755 %{buildroot}%{_bindir}
cp -r tools data %{buildroot}%{_libdir}/waydroid/
mv data/Waydroid.desktop %{buildroot}%{_datadir}/applications
cp waydroid.py %{buildroot}%{_libdir}/waydroid
ln -s %{_libdir}/waydroid/waydroid.py %{buildroot}%{_bindir}/waydroid

install -Dm644 -t %{buildroot}%{_sysconfdir}/gbinder.d gbinder/anbox.conf
install -Dm644 -t %{buildroot}%{_unitdir} debian/waydroid-container.service

%post
%systemd_post waydroid-container.service
%systemd_user_post anbox-session-manager.service

%preun
%systemd_preun waydroid-container.service
%systemd_user_preun anbox-session-manager.service

%postun
%systemd_postun_with_restart waydroid-container.service

%files
%{_sysconfdir}/gbinder.d
%{_bindir}/waydroid
%{_unitdir}/waydroid-container.service
%{_libdir}/waydroid/
%{_datadir}/applications/Waydroid.desktop

%changelog
* Wed Sep 21 03:29:15 CST 2021 gzzchh <xjdzch@126.com> - 0-0.1.20190721gitcd829e9
- Initial package