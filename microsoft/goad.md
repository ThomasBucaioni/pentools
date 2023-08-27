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

```
mkdir vagrant-testdir
cd vagrant-testdir
vagrant init fedora/38-cloud-base
vagrant up --provider=libvirt
```
Check in `virt-manager` that the VM `fedora/38-cloud-base` appears

## GOAD install




