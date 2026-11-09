Name:           kansora-dots
Version:        0.2.0
# The Makefile rewrites Release to <commit-count>.git<sha> so every push upgrades.
Release:        1%{?dist}
Summary:        Default dotfiles for Kansora, managed with mise
# No licence chosen; rpmbuild needs a value here.
License:        LicenseRef-Not-Licensed
URL:            https://github.com/euandeas/kdots
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

# Renamed from Hafnium in 0.2.0: replace the old packages on upgrade
Obsoletes:      hafnium-dots < 0.2
Provides:       hafnium-dots = %{version}-%{release}

BuildRequires:  systemd-rpm-macros

Requires:       mise
Requires:       jq
Requires:       niri
Requires:       ghostty
Requires:       fastfetch

%description
Kansora's default user configuration (niri, DMS keybinds, Ghostty), deployed
with mise's dotfiles support. Defaults ship as a mise system config layer
(/etc/mise/conf.d/kansora.toml), so a personal mise config can override any
entry. A user service deploys missing files at login and never overwrites
files you have changed.

%prep
%autosetup -n %{name}-%{version}

%build

%install
install -Dpm0644 mise/kansora.toml          %{buildroot}%{_sysconfdir}/mise/conf.d/kansora.toml
install -Dpm0755 bin/kansora-dots           %{buildroot}%{_bindir}/kansora-dots
install -Dpm0644 systemd/kansora-dots.service   %{buildroot}%{_userunitdir}/kansora-dots.service
install -Dpm0644 systemd/80-kansora-dots.preset %{buildroot}%{_userpresetdir}/80-kansora-dots.preset
install -Dpm0644 fastfetch/config.jsonc     %{buildroot}%{_sysconfdir}/xdg/fastfetch/config.jsonc
install -d %{buildroot}%{_datadir}/kansora/dots
cp -a dots/. %{buildroot}%{_datadir}/kansora/dots/

%post
%systemd_user_post kansora-dots.service

%preun
%systemd_user_preun kansora-dots.service

%files
%doc README.md
# Not noreplace: this is Kansora's layer. Override entries in ~/.config/mise/config.toml instead.
%config %{_sysconfdir}/mise/conf.d/kansora.toml
# System-wide default; users override it with ~/.config/fastfetch/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%{_bindir}/kansora-dots
%{_userunitdir}/kansora-dots.service
%{_userpresetdir}/80-kansora-dots.preset
%dir %{_datadir}/kansora
%{_datadir}/kansora/dots/

%changelog
* Sun Nov 08 2026 euandeas - 0.1.0-1
- Initial package
