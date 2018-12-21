# Copyright (c) 2015-2018, Nicolas Chauvet <kwizart@gmail.com>
# All rights reserved.

%global commit0 f54766b21d216584a6839340aa1ebf81a980b235
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%{!?_cuda_version_rpm:
%global _cuda_version_rpm 6-5
}

Name:           gdrcopy
Version:        1.4
Release:        3%{?dist}
Summary:        A fast GPU memory copy library based on NVIDIA GPUDirect RDMA technology

License:        MIT
URL:            https://github.com/NVIDIA/gdrcopy
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# Should be supported on ppc64le, but no public driver yet
ExclusiveArch:  x86_64

#We need the cuda toolkit
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cuda-compiler-%{?_cuda_version_rpm}
BuildRequires:  cuda-libraries-dev-%{?_cuda_version_rpm}

BuildRequires:  cuda-drivers-devel
Requires:       cuda-drivers%{_isa}

#Kmod handle
Requires:       %{name}-kmod >= %{version}
Provides:       %{name}-kmod-common >= %{version}

# We need to filter libcudart
%if (0%{?fedora} || 0%{?rhel} > 6)
%global __requires_exclude ^libcudart.*$
%else
%{?filter_setup:
%filter_from_requires /libcudart.so.*/d
%filter_setup
}
%endif


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
%autosetup -n %{name}-%{commit0}


%build
%make_build \
  COMMONCFLAGS="%{optflags}" \
  %{?_cuda_prefix:CUDA=%{?_cuda_prefix}} \
  config lib exes


%install
%make_install PREFIX=%{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
install -pm 755 basic validate copybw %{buildroot}%{_libexecdir}/%{name}

chmod 0755 %{buildroot}%{_libdir}/libgdrapi.so.1*


%ldconfig_scriptlets


%files
%license LICENSE
%doc README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/basic
%{_libexecdir}/%{name}/copybw
%{_libexecdir}/%{name}/validate
%{_libdir}/libgdrapi.so.1*

%files devel
%{_includedir}/gdrapi.h
%{_libdir}/libgdrapi.so


%changelog
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
