%global     forgeurl    https://github.com/gzzchh/netfilter-full-cone-nat
%global     commit      a238afb7bd4533a0aba4024a79f85841a3d80d85
%forgemeta -i

Name:       netfilter-fullcone-dkms
Version:    1
Release:    0%{?dist}
Summary:    Kernel Module for netfilter-fullcone nat

License:    GPLv3+
URL:        %{forgeurl}
Source:     %{forgesource}


Requires:       gcc, make, perl, diffutils
Requires:       kernel-devel
Requires:       dkms
BuildRequires:  git


%description
让你的 iptables 支持 FullConeNAT 所需的内核模块

%define dkms_src_dir   %{name}-%{commit}

%prep
rm -rf %{dkms_src_dir}
git clone --recurse-submodules %{forgeurl}.git %{dkms_src_dir}
cd %{dkms_src_dir}
git checkout %{commit}

%build
cd %{dkms_src_dir}
# 没有构建

%install
cd %{dkms_src_dir}
# 只是放文件
install -dm755 %{buildroot}%{_usrsrc}/xt_FULLCONENAT-1.0
install -Dm644 xt_FULLCONENAT.c %{buildroot}%{_usrsrc}/xt_FULLCONENAT-1.0
install -Dm644 Makefile %{buildroot}%{_usrsrc}/xt_FULLCONENAT-1.0
install -Dm644 dkms.conf %{buildroot}%{_usrsrc}/xt_FULLCONENAT-1.0

%post -p /bin/sh
if [[ ! -e "%{_usrsrc}/xt_FULLCONENAT-1.0" ]];then
    # 模块源码不存在
    # echo ""
    dkms add -m xt_FULLCONENAT -v 1.0 || true
fi
dkms build -m xt_FULLCONENAT -v 1.0 || true
dkms install -m xt_FULLCONENAT -v 1.0 --force || true
# 尝试加载
modprobe xt_FULLCONENAT || true

%preun -p /bin/sh
rmmod xt_FULLCONENAT
# 需要手工确定一下 M 的定义
dkms uninstall -m xt_FULLCONENAT -v "1.0" --all || true
dkms remove -m xt_FULLCONENAT -v "1.0" --all || true


%files
%{_usrsrc}/xt_FULLCONENAT-1.0

%changelog
* Wed Sep 22 03:29:15 CST 2021 gzzchh <xjdzch@126.com> - 0-0.1.20190721gitcd829e9
- Initial package