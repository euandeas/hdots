Name:           hafnium-dots
Version:        0.1.0
# The Makefile rewrites Release to <commit-count>.git<sha> so every push upgrades.
Release:        1%{?dist}
Summary:        Default dotfiles for Hafnium, managed with mise
# No licence chosen; rpmbuild needs a value here.
License:        LicenseRef-Not-Licensed
URL:            https://github.com/euandeas/hdots
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  systemd-rpm-macros

Requires:       mise
Requires:       jq
Requires:       niri
Requires:       ghostty
Requires:       fastfetch

%description
Hafnium's default user configuration (niri, DMS keybinds, Ghostty), deployed
with mise's dotfiles support. Defaults ship as a mise system config layer
(/etc/mise/conf.d/hafnium.toml), so a personal mise config can override any
entry. A user service deploys missing files at login and never overwrites
files you have changed.

%prep
%autosetup -n %{name}-%{version}

%build

%install
install -Dpm0644 mise/hafnium.toml          %{buildroot}%{_sysconfdir}/mise/conf.d/hafnium.toml
install -Dpm0755 bin/hafnium-dots           %{buildroot}%{_bindir}/hafnium-dots
install -Dpm0644 systemd/hafnium-dots.service   %{buildroot}%{_userunitdir}/hafnium-dots.service
install -Dpm0644 systemd/80-hafnium-dots.preset %{buildroot}%{_userpresetdir}/80-hafnium-dots.preset
install -Dpm0644 fastfetch/config.jsonc     %{buildroot}%{_sysconfdir}/xdg/fastfetch/config.jsonc
install -d %{buildroot}%{_datadir}/hafnium/dots
cp -a dots/. %{buildroot}%{_datadir}/hafnium/dots/

%post
%systemd_user_post hafnium-dots.service

%preun
%systemd_user_preun hafnium-dots.service

%files
%doc README.md
# Not noreplace: this is Hafnium's layer. Override entries in ~/.config/mise/config.toml instead.
%config %{_sysconfdir}/mise/conf.d/hafnium.toml
# System-wide default; users override it with ~/.config/fastfetch/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%{_bindir}/hafnium-dots
%{_userunitdir}/hafnium-dots.service
%{_userpresetdir}/80-hafnium-dots.preset
%dir %{_datadir}/hafnium
%{_datadir}/hafnium/dots/

%changelog
* Sun Nov 08 2026 euandeas - 0.1.0-1
- Initial package
