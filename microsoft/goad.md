# Game Of Active Directory install

## Vagrant install for libvirt

https://vagrant-libvirt.github.io/vagrant-libvirt/

### Vagrant installation

```
sudo dnf remove vagrant-libvirt
sudo sed -i '/^\(exclude=.*\)/ {/vagrant-libvirt/! s//\1 vagrant-libvirt/;:a;n;ba;q}; $aexclude=vagrant-libvirt' /etc/dnf/dnf.conf
vagrant_libvirt_deps=($(sudo dnf repoquery --disableexcludes main --depends vagrant-libvirt 2>/dev/null | cut -d' ' -f1))
dependencies=$(sudo dnf repoquery --qf "%{name}" ${vagrant_libvirt_deps[@]/#/--whatprovides })
sudo dnf install --assumeyes @virtualization ${dependencies}
```

### Vagrant-libvirt installation

```
vagrant plugin install vagrant-libvirt
```

### Spawn a VM (Fedora 38)

Or pick another image: https://app.vagrantup.com/fedora/
```
mkdir vagrant-testdir
cd vagrant-testdir
vagrant init fedora/38-cloud-base
vagrant up --provider=libvirt
```
Check in `virt-manager` that the VM `fedora/38-cloud-base` appears. Root login: `root/vagrant`

## GOAD install

https://github.com/Orange-Cyberdefense/GOAD

### In `Vagrantfile`

#### Environment variable `VAGRANT_DEFAULT_PROVIDER`

Replace the line
```
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'
```
with 
```
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'
```
(see also https://vagrant-libvirt.github.io/vagrant-libvirt/#start-vm environment variable `VAGRANT_DEFAULT_PROVIDER`). 

#### VM `cpu` and `memory` configuration

Then replace
```
  config.vm.provider "virtualbox" do |v|
    v.memory = 4000
    v.cpus = 2
  end
```
with 
```
  config.vm.provider "libvirt" do |v|
    v.memory = 4000
    v.cpus = 2
  end
```
(see also https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html#domain-specific-options fields `cpu` and `memory`)

#### Vagrant `winrm` plugin

Also install the `winrm` plugin: https://stackoverflow.com/questions/35016414/vagrant-up-fails-with-cannot-load-winrm
```
vagrant plugin install winrm
vagrant plugin install winrm-fs
vagrant plugin install winrm-elevated
```

#### Unsupported boxes

Then, install the `vagrant-mutate` plugin: https://medium.com/@gamunu/use-vagrant-with-libvirt-unsupported-boxes-12e719d71e8e
```
sudo yum install qemu-img libvirt-devel rubygem-ruby-libvirt ruby-devel redhat-rpm-config
vagrant plugin install vagrant-mutate
```
Then download the GOAD boxes and mutate them:
```
vagrant box add --provider virtualbox StefanScherer/windows_2016
vagrant box add --provider virtualbox StefanScherer/windows_2019
vagrant mutate StefanScherer/windows_2016 libvirt
vagrant mutate StefanScherer/windows_2019 libvirt
```
and check the list: `vagrant box list`

### Networking

In `ad/sevenkingdoms.local/inventory`, change the lines:
```
; adapter created by vagrant and virtualbox
nat_adapter=Ethernet
domain_adapter=Ethernet 2

; adapter created by vagrant and vmware
; nat_adapter=Ethernet0
; domain_adapter=Ethernet1
```
with
```
; adapter created by vagrant and virtualbox
; nat_adapter=Ethernet
; domain_adapter=Ethernet 2

; adapter created by vagrant and libvirt
nat_adapter=Ethernet0
domain_adapter=Ethernet1
```
(to check...)

