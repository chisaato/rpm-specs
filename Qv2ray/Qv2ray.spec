
%global forgeurl https://github.com/Qv2ray/Qv2ray
Version: 2.7.0

%forgemeta

%define interface_version 3

Name:           Qv2ray
Release:        0
Summary:        Unleash Your V2Ray
License:        GPL-3.0-only
Group:          Productivity/Networking/Web/Proxy
URL:	        %{forgeurl}
Source:         %{forgesource}
%if 0%{?suse_version}
# for openSUSE
BuildRequires:  libqt5-qtbase-common-devel >= 5.11
BuildRequires:  libQt5Core-devel
BuildRequires:  libQt5Gui-devel
BuildRequires:  libQt5Network-devel
BuildRequires:  libQt5Widgets-devel
BuildRequires:  libQt5Concurrent-devel
BuildRequires:  libqt5-linguist-devel
BuildRequires:  libqt5-qtsvg-devel
BuildRequires:  grpc-devel
BuildRequires:  update-desktop-files
BuildRequires:  golang-packaging
BuildRequires:  ninja
%if 0%{?suse_version} >= 1550
## for abseil-cpp about absl::xx realted not found
## maybe related upstream change: https://build.opensuse.org/package/rdiff/devel:tools/grpc?linkrev=base&rev=72
BuildRequires:  abseil-cpp-devel
%endif
%else
# for Fedora/CentOS/ ...
BuildRequires:  qt5-qtbase-devel >= 5.11
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  grpc-devel
BuildRequires:  grpc-plugins
BuildRequires:  glibc-langpack-en
BuildRequires:  desktop-file-utils
BuildRequires:  ninja-build
BuildRequires:  cmake

%endif
BuildRequires:  protobuf-devel
BuildRequires:  libcurl-devel

Requires:       openssl
Conflicts:      Qv2ray-preview
Provides:       Qv2ray-Plugin-Interface = %{interface_version}
%if 0%{?suse_version} || 0%{?fedora_version} || 0%{?centos_version} >= 800 
Recommends:     v2ray-core
%endif

%description
Qv2ray, A Qt frontend for v2ray. Written in c++.
Features:
    * Cross-platform, multi-distribution support
    * Versatile Host Importing
    * Subscriptions
    * Built-in Host Editors
    * (Almost) Full Functionality Support
    * Real-time Speed & Data Usage Monitoring
    * Latency Testing (TCP) 
More detail Please check https://qv2ray.github.io

%prep
%forgesetup
%define BUILD_SOURCE %{_builddir}/%{name}-%{version}
%define BUILD_DIR %{_builddir}/%{name}-%{version}/build
mkdir -p %{BUILD_DIR}
# 准备子模块
cd  %{_builddir}/%{name}-%{version}
if [ ! -d .git ]; then
    git clone --bare --depth 1 %{forgeurl}.git .git
    git config --local --bool core.bare false
    git reset --hard
fi
git submodule foreach --recursive git submodule init
git submodule update --init --recursive

%build
# build
export _QV2RAY_BUILD_INFO_="Qv2ray built by Fedora Copr"
export _QV2RAY_BUILD_EXTRA_INFO_="(Official Build) $(uname -a | cut -d ' ' -f3,13), Qt $(pkg-config --modversion Qt5Core)"
%cmake \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DQV2RAY_TRANSLATION_PATH="/usr/share/qv2ray/lang" \
    -DQV2RAY_DEFAULT_VCORE_PATH="/usr/bin/v2ray" \
    -DQV2RAY_DEFAULT_VASSETS_PATH="/usr/share/v2ray" \
    -DQV2RAY_DISABLE_AUTO_UPDATE=ON \
    -DQV2RAY_ZXING_PROVIDER="module" \
    -DCMAKE_BUILD_TYPE=Release \
    -GNinja
%cmake_build

%install
%cmake_install

%post
%postun

%files
%license LICENSE
%doc README.md
%{_bindir}/qv2ray
%{_datadir}/applications/qv2ray.desktop
%{_datadir}/icons/hicolor
%{_datadir}/metainfo/qv2ray.metainfo.xml
%{_datadir}/qv2ray/lang/*.qm
%{_datadir}/qv2ray/plugins/*
%dir %{_datadir}/qv2ray
%dir %{_datadir}/qv2ray/lang
%dir %{_datadir}/qv2ray/plugins

%changelog