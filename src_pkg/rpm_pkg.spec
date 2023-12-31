%define module module-name

#
# spec file for package tuxedo-keyboard-ite
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Summary:        Keyboard back-light driver for ITE devices
Name:           %{module}
Version:        x.x.x
Release:        x
License:        GPLv3+
Group:          Hardware/Other
BuildArch:      noarch
Url:            https://www.tuxedocomputers.com
Source:         %{module}-%{version}.tar.bz2
Requires:       dkms >= 1.95
BuildRoot:      %{_tmppath}
Packager:       TUXEDO Computers GmbH <tux@tuxedocomputers.com>

%description
USB HID driver for ITE devices on TUXEDO laptops.
This module provides back-light control for ITE Device(829x).

%prep
%setup -n %{module}-%{version} -q

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}/
cp dkms.conf Makefile %{buildroot}/usr/src/%{module}-%{version}
cp -R src/ %{buildroot}/usr/src/%{module}-%{version}
mkdir -p %{buildroot}/usr/share/
mkdir -p %{buildroot}/usr/share/%{module}/
cp postinst %{buildroot}/usr/share/%{module}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) /usr/src/%{module}-%{version}/
%attr(0644,root,root) /usr/src/%{module}-%{version}/*
%attr(0755,root,root) /usr/src/%{module}-%{version}/src/
%attr(0644,root,root) /usr/src/%{module}-%{version}/src/*
%attr(0755,root,root) /usr/share/%{module}/
%attr(0755,root,root) /usr/share/%{module}/postinst
%license LICENSE

%post
for POSTINST in /usr/lib/dkms/common.postinst /usr/share/%{module}/postinst; do
    if [ -f $POSTINST ]; then
        $POSTINST %{module} %{version} /usr/share/%{module}
        RET=$?
        rmmod ite_829x > /dev/null 2>&1 || true
        modprobe ite_829x > /dev/null 2>&1 || true
        rmmod ite_8297 > /dev/null 2>&1 || true
        modprobe ite_8297 > /dev/null 2>&1 || true
        rmmod ite_8291 > /dev/null 2>&1 || true
        modprobe ite_8291 > /dev/null 2>&1 || true
        rmmod ite_8291_lb > /dev/null 2>&1 || true
        modprobe ite_8291_lb > /dev/null 2>&1 || true
        exit $RET
    fi
    echo "WARNING: $POSTINST does not exist."
done

echo -e "ERROR: DKMS version is too old and %{module} was not"
echo -e "built with legacy DKMS support."
echo -e "You must either rebuild %{module} with legacy postinst"
echo -e "support or upgrade DKMS to a more current version."
exit 1


%preun
echo -e
echo -e "Uninstall of %{module} module (version %{version}-%{release}) beginning:"
dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
if [ $1 != 1 ];then
    /usr/sbin/rmmod ite_829x > /dev/null 2>&1 || true
    /usr/sbin/rmmod ite_8297 > /dev/null 2>&1 || true
    /usr/sbin/rmmod ite_8291 > /dev/null 2>&1 || true
    /usr/sbin/rmmod ite_8291_lb > /dev/null 2>&1 || true
fi
exit 0


%changelog
* Thu Nov 16 2023 C Sandberg <tux@tuxedocomputers.com> 0.4.4-1
- Add color scaling for Stellaris Gen5 AMD devices
* Thu Aug 03 2023 C Sandberg <tux@tuxedocomputers.com> 0.4.3-1
- Adjusted lightbar USB product exclusion (prevents driver binding to unused 
  devices) for Stellaris Gen5 and allows proper binding of relevant ones.
- Lightbar color scaling for Stellaris 17 Gen5
* Thu May 04 2023 C Sandberg <tux@tuxedocomputers.com> 0.4.1-1
- Four zone backlight support for Stellaris Gen5
- Experimental buffered writes for Stellaris/Fusion per-key variants
* Mon Apr 17 2023 C Sandberg <tux@tuxedocomputers.com> 0.4.0-1
- Color scaling for Stellaris Intel Gen5
- Lightbar impl. for Stellaris Gen4/5
* Thu Feb 23 2023 C Sandberg <tux@tuxedocomputers.com> 0.3.0-1
- Leds interface support (/sys/class/leds)
* Wed Dec 07 2022 C Sandberg <tux@tuxedocomputers.com> 0.2.5-1
- Add per-device color scaling to ite_8291 driver
- Add additional scaling setting for Stellaris 17 AMD Gen 4
* Wed Nov 30 2022 C Sandberg <tux@tuxedocomputers.com> 0.2.4-1
- Add USB ID for Stellaris 17 Gen 4 keyboard backlight
* Mon Feb 22 2021 C Sandberg <tux@tuxedocomputers.com> 0.2.3-1
- Fix broken brightness key reaction for ite_829x
* Tue Feb 16 2021 C Sandberg <tux@tuxedocomputers.com> 0.2.2-1
- Attempt to fix ite_829x instability sometimes locking up kernel on keypress
* Mon Dec 21 2020 C Sandberg <tux@tuxedocomputers.com> 0.2.1-1
- Added device 048d:6004 to ite_8291
* Fri Nov 13 2020 C Sandberg <tux@tuxedocomputers.com> 0.2.0-1
- Added initial support for ITE Device(8291) ->  048d:ce00
* Fri Oct 16 2020 C Sandberg <tux@tuxedocomputers.com> 0.1.0-1
- Added initial (very basic) support for 048d:8297 LED controller
* Mon Oct 12 2020 C Sandberg <tux@tuxedocomputers.com> 0.0.3-1
- Fixed key mapping toggle <=> switch mode
- Default color to white
* Tue Sep 29 2020 C Sandberg <tux@tuxedocomputers.com> 0.0.2-1
- Initial experimental release
* Thu Apr 23 2020 C Sandberg <tux@tuxedocomputers.com> 0.0.1-1
- First version of the ITE keyboard backlight driver
- Has support for ITE Device(829x) ->  0x048d:0x8910
