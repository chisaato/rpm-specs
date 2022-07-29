# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global gittag 3.0.10
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:       tuxedo-keyboard-kmod
Summary:    Kernel module (kmod) for Tuxedo Keyboard
Version:    %{gittag}
Release:    1%{?dist}
License:    GPLv3
URL:	    https://github.com/tuxedocomputers/tuxedo-keyboard
Source:     https://github.com/tuxedocomputers/tuxedo-keyboard/archive/refs/tags/v%{version}.zip


BuildRequires:    %{_bindir}/kmodtool
%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo copr --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel module for keyboard backlighting on TUXEDO Computers

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo copr --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup
for kernel_version in %{?kernel_versions} ; do
    cp -a xtables-addons-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    # export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" \
    M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p  $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 0755 _kmod_build_${kernel_version%%___*}/extensions/*.ko \
         $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog