# Copyright (c) 2015-2021, Nicolas Chauvet <kwizart@gmail.com>
# All rights reserved.

# If _cuda_version is unset
%if 0%{!?_cuda_version:1}
%global _cuda_version 11.2
%global _cuda_rpm_version 11-2
%global _cuda_prefix /usr/local/cuda-%{_cuda_version}
%endif

Name:           gdrcopy
Version:        2.2
Release:        1%{?dist}
Summary:        A fast GPU memory copy library based on NVIDIA GPUDirect RDMA technology

License:        MIT
URL:            https://github.com/NVIDIA/gdrcopy
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Should be supported on ppc64le, but no public driver yet
ExclusiveArch:  x86_64

#We need the cuda toolkit
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cuda-compiler-%{?_cuda_rpm_version}
BuildRequires:  cuda-cudart-devel-%{?_cuda_rpm_version}
BuildRequires:  cuda-driver-devel-%{?_cuda_rpm_version}
BuildRequires:  check-devel

BuildRequires:  cuda-drivers-devel
Requires:       cuda-drivers%{_isa}

#Kmod handle
Requires:       %{name}-kmod >= %{version}
Provides:       %{name}-kmod-common = %{version}


%description
While GPUDirect RDMA is meant for direct access to GPU memory from
third-party devices, it is possible to use these same APIs to create
perfectly valid CPU mappings of the GPU memory.

The advantage of a CPU driven copy is the essencially zero latency
involved in the copy process. This might be useful when low latencies
are required.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%make_build \
  COMMONCFLAGS="%{optflags}" \
  %{?_cuda_prefix:CUDA=%{?_cuda_prefix}} \
  config lib exes


%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}
%make_install prefix=%{_prefix} libdir=%{_libdir} DESTBIN=%{buildroot}%{_libexecdir}/%{name}

chmod 0755 %{buildroot}%{_libdir}/libgdrapi.so.2*


%ldconfig_scriptlets


%files
%license LICENSE
%doc README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/copybw
%{_libexecdir}/%{name}/copylat
%{_libexecdir}/%{name}/sanity
%{_libdir}/libgdrapi.so.2*

%files devel
%{_includedir}/gdrapi.h
%{_libdir}/libgdrapi.so


%changelog
* Fri Mar 12 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.2-1
- Update to 2.2

* Thu Feb 06 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.0-1
- Update to 2.0

* Tue Dec 18 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.4-3
- Set exec perm on library

* Mon Dec 17 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.4-2
- Add default _cuda_version_rpm

* Fri Dec 07 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.4-1
- Update to 1.4
- Drop support for i686

* Fri Apr 07 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.2-1
- Update to 1.2

* Wed Feb 25 2015 Nicolas Chauvet <kwizart@gmail.com> - 0-1
- Initial spec file
