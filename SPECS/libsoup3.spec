## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 11;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global glib2_version 2.69.1

Name:    libsoup3
Version: 3.6.5
Release: 3%{?dist}.%{autorelease -n}
Summary: Soup, an HTTP library implementation

License: LGPL-2.0-or-later
URL:     https://wiki.gnome.org/Projects/libsoup
Source0: https://download.gnome.org/sources/libsoup/3.6/libsoup-%{version}.tar.xz

# Downstream patch, needed due to glib2 gnutls-hmac.patch
Patch:   no-ntlm-in-fips-mode.patch

# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/426
Patch:   test-timeouts.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/454
Patch:   server-test-timeout.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/455
Patch:   http2-body-size-test-timeout.patch

# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/450
Patch:   CVE-2025-32914.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/451
Patch:   CVE-2025-32908.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/448 (simplified and corrected)
Patch:   CVE-2025-4035.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/463
Patch:   CVE-2025-4948.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/408 (simplified)
Patch:   CVE-2025-32049.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/452
Patch:   CVE-2025-32907.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/473
Patch:   CVE-2025-4945-CVE-2025-11021.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/481
Patch:   CVE-2025-12105.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/491
Patch:   CVE-2025-14523.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/494
Patch:   CVE-2026-0719.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/496
Patch:   CVE-2026-1761.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/516
Patch:   CVE-2026-5119.patch
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/511
Patch:   CVE-2026-4271.patch

BuildRequires: ca-certificates
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: glib-networking
BuildRequires: gi-docgen >= 2021.1
BuildRequires: krb5-devel
BuildRequires: meson
BuildRequires: vala
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libbrotlidec)
BuildRequires: pkgconfig(libnghttp2)
BuildRequires: pkgconfig(libpsl)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: /usr/bin/ntlm_auth

Recommends: glib-networking%{?_isa} >= %{glib2_version}

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it), but the SOAP parts were removed
long ago.

%package devel
Summary: Header files for the Soup library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%package doc
Summary: Documentation files for %{name}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts
BuildArch: noarch

%description doc
This package contains developer documentation for %{name}.

%prep
%autosetup -p1 -n libsoup-%{version}

%build
%meson -Ddocs=enabled -Dautobahn=disabled
%meson_build

%install
%meson_install
install -m 644 -D tests/libsoup.supp %{buildroot}%{_datadir}/libsoup-3.0/libsoup.supp

%check
%meson_test

%find_lang libsoup-3.0

%files -f libsoup-3.0.lang
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/libsoup-3.0.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Soup-3.0.typelib

%files devel
%{_includedir}/libsoup-3.0
%{_libdir}/libsoup-3.0.so
%{_libdir}/pkgconfig/libsoup-3.0.pc
%dir %{_datadir}/libsoup-3.0
%{_datadir}/libsoup-3.0/libsoup.supp
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Soup-3.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libsoup-3.0.deps
%{_datadir}/vala/vapi/libsoup-3.0.vapi

%files doc
%{_docdir}/libsoup-3.0/

%changelog
## START: Generated by rpmautospec
* Mon May 04 2026 Michael Catanzaro <mcatanzaro@gnome.org> - 3.6.5-11
- Add patches for CVE-2026-4271 and CVE-2026-5119

* Mon Feb 02 2026 Michael Catanzaro <mcatanzaro@gnome.org> - 3.6.5-10
- Add patch for CVE-2026-1761

* Fri Jan 30 2026 Michael Catanzaro <mcatanzaro@gnome.org> - 3.6.5-9
- Fix CVE-2026-0719

* Wed Jan 07 2026 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-8
- Fix CVE-2025-14523

* Thu Dec 11 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-7
- Add patch for CVE-2025-12105

* Tue Dec 09 2025 RHEL Packaging Agent <jotnar@redhat.com> - 3.6.5-6
- Fix integer overflow in date/time parsing

* Tue May 27 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-5
- Bump revision number

* Wed May 21 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-4
- Fix several CVEs

* Thu May 01 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-3
- Add patch to hopefully fix http2-body-size-test timeouts

* Wed Apr 30 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-2
- Add patch to hopefully fix server-test timeouts

* Tue Apr 29 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.5-1
- Update to 3.6.5 and add patches for CVEs

* Wed Jan 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.3-1
- Update to 3.6.3

* Fri Jan 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 3.4.4-6
- Bump release for October 2024 mass rebuild:

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 3.4.4-5
- Bump release for June 2024 mass rebuild

* Thu Apr 25 2024 Tomas Pelka <tpelka@redhat.com> - 3.4.4-4
- Add gating.yaml via API

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.4.4-1
- 3.4.4

* Fri Sep 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.4.3-1
- 3.4.3

* Fri Aug 25 2023 Adam Williamson <awilliam@redhat.com> - 3.4.2-4
- Backport MR #374 to fix some crashes

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 David King <amigadave@amigadave.com> - 3.4.2-2
- Drop reverted patch

* Tue May 02 2023 David King <amigadave@amigadave.com> - 3.4.2-1
- Update to 3.4.2

* Fri Apr 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.4.1-2
- Add patch to maybe fix connection crashes?

* Fri Apr 21 2023 David King <amigadave@amigadave.com> - 3.4.1-1
- Update to 3.4.1

* Sat Mar 18 2023 W. Michael Petullo <mike@flyn.org> - 3.4.0-2
- Distribute libsoup.supp

* Fri Mar 17 2023 David King <amigadave@amigadave.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.3.1-2
- migrated to SPDX license

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 3.3.1-1
- Update to 3.3.1

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.2.2-2
- Ensure correct fonts are installed for HTML docs

* Thu Nov 03 2022 David King <amigadave@amigadave.com> - 3.2.2-1
- Update to 3.2.2

* Fri Oct 28 2022 David King <amigadave@amigadave.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2022 Kalev Lember <klember@redhat.com> - 3.2.0-2
- Backport upstream MR310 to fix gnome-maps crashes (#2129914)

* Fri Sep 16 2022 Kalev Lember <klember@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Aug 15 2022 Kalev Lember <klember@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Mon Aug 15 2022 Kalev Lember <klember@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 David King <amigadave@amigadave.com> - 3.1.1-1
- Update to 3.1.1

* Wed Jul 06 2022 David King <amigadave@amigadave.com> - 3.0.7-1
- Update to 3.0.7

* Tue Apr 26 2022 Adam Williamson <awilliam@redhat.com> - 3.0.6-3
- Revert "Backport MR #281 to fix a crash (#2070240)"

* Tue Apr 26 2022 Adam Williamson <awilliam@redhat.com> - 3.0.6-2
- Backport MR #281 to fix a crash (#2070240)

* Fri Apr 01 2022 David King <amigadave@amigadave.com> - 3.0.6-1
- Update to 3.0.6

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 3.0.5-1
- Update to 3.0.5

* Tue Jan 25 2022 Patrick Griffis <tingping@fedoraproject.org> - 3.0.4-2
- Remove unecessary dependencies

* Wed Jan 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.0.4-1
- Initial import.
## END: Generated by rpmautospec
