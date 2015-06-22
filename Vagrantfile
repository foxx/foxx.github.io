# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provision "shell", path: "provision.sh"
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.provider "vmware_fusion" do |vm, override|
    override.vm.box = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vmwarefusion.box"
    vm.memory = 1048
    vm.cpus = 2

    # Mount using NFS due to problems with fs performance and
    # random guest addition crashes. This should fall back to
    # shared folders on Windows
    config.vm.synced_folder ".", "/vagrant", type: "nfs"
  end

  config.vm.provider "virtualbox" do |vm, override|
    override.vm.box = "ubuntu/trusty64"
    vm.memory = 1048
    vm.cpus = 2
  end
end
