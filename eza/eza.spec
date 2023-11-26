
%global crate eza

Name:           eza
Version:        0.16.1
Release:        1%{?dist}
Summary:        Modern replacement for ls

License:        MIT
URL:            https://github.com/eza-community/eza
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
# Automatically generated patch to strip dependencies and normalize metadata
# Patch:          eza-fix-metadata-auto.diff

BuildRequires:  rust
BuildRequires:  cargo

%global _description %{expand:
A modern replacement for ls.}

%description
%{_description}


%prep
%autosetup -n %{name}-%{version}

%build

cargo build -j$(nproc) --release

%install
install -D -m 0755 target/release/eza %{buildroot}%{_bindir}/eza
# 还需要安装各种补全
# Fish 的位于 share/fish/vendor_completions.d/eza.fish
# Zsh 的位于 share/zsh/site-functions/_eza
# Bash 的位于 share/bash-completion/completions/_eza
install -D -m 0644 completions/bash/eza %{buildroot}%{_datadir}/bash-completion/completions/_eza
install -D -m 0644 completions/fish/eza.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/eza.fish
install -D -m 0644 completions/zsh/_eza %{buildroot}%{_datadir}/zsh/site-functions/_eza

%files
%{_bindir}/eza
%{_datadir}/bash-completion/completions/_eza
%{_datadir}/fish/vendor_completions.d/eza.fish
%{_datadir}/zsh/site-functions/_eza