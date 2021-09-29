# tests are enabled by default
%bcond_without tests

%global         srcname     proto-plus
%global         forgeurl    https://github.com/googleapis/proto-plus-python
Version:        1.19.2
%forgemeta

Name:           python-%{srcname}
Release:        %autorelease
Summary:        Python wrapper around protocol buffers

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
This is a wrapper around protocol buffers. Protocol buffers is a specification
format for APIs, such as those inside Google. This library provides protocol
buffer message classes and objects that largely behave like native Python
types.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%description -n python3-%{srcname} %{_description}


%package -n python3-%{srcname}-doc
Requires:       python3-docs
BuildRequires:  python3-docs
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
Summary:        Documentation for python-%{srcname}

%description -n python3-%{srcname}-doc
Documentation for python-%{srcname}


%prep
%forgeautosetup


%generate_buildrequires
%pyproject_buildrequires -x testing


%build
%pyproject_wheel

# Generate documentation.
PYTHONPATH="${PWD}:${PWD}/docs/" sphinx-build docs html %{?_smp_mflags}
rm -rf html/.{doctrees,buildinfo,nojekyll}


%install
%pyproject_install
%pyproject_save_files proto


%if %{with tests}
%check
%pytest tests
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
%autochangelog
