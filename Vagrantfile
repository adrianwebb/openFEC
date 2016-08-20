
require 'yaml'

vm_config = YAML.load_file("vagrant-config.default.yml")
vm_config.merge!(YAML.load_file("vagrant-config.yml")) if File.exist?("vagrant-config.yml")

required_plugins = %w(vagrant-vbguest)
project_directory = '/home/vagrant/app'

required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = vm_config["server_name"]

  config.vm.network "private_network", ip: vm_config["ip_address"]

  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", project_directory, owner: "vagrant", group: "vagrant", mount_options: ["dmode=775"]
  
  config.vm.network "forwarded_port", guest: 8080, host: vm_config["host_http_port"]
  config.vm.network "forwarded_port", guest: 5432, host: vm_config["host_db_port"]
  
  config.vm.provider "virtualbox" do |v|
    v.name = vm_config["server_name"]
    v.cpus = vm_config["cpus"]
    v.memory = vm_config["memory_size"]
  end
  
  config.vm.provision "shell", inline: "initctl emit vagrant-ready", run: "always"
  
  config.vm.provision "shell" do |s|
    s.name = "Create swap space"
    s.inline = <<-SHELL
      set -e

      memory_size="${1}"
      swap_size=$((${memory_size}*2))
      
      swapoff -a
      
      fallocate -l "${swap_size}m" /swapfile
      chmod 600 /swapfile
      mkswap /swapfile
      swapon /swapfile
      echo "/swapfile none swap sw 0 0" >> /etc/fstab
      
      sysctl vm.swappiness=10
      echo "vm.swappiness=10" >> /etc/sysctl.conf
      
      sysctl vm.vfs_cache_pressure=50
      echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf
    SHELL
    
    s.args = [
      vm_config["memory_size"],
    ] 
  end
  
  config.vm.provision "shell" do |s|
    s.name = "Initialize Docker and Docker Compose"
    s.inline = <<-SHELL
      set -e
      
      if [ "`which docker`" == "" ]; then
        echo "Preparing Docker environment"
        apt-get update
        apt-get install -y lxc wget bsdtar curl
        apt-get install -y linux-image-extra-$(uname -r)
        modprobe aufs
      
        echo "Installing Docker"
        wget -qO- https://get.docker.com/ | sh
        sed -i "s/^start on (local-filesystems and net-device-up IFACE!=lo)/start on vagrant-ready/" /etc/init/docker.conf
        usermod -aG docker vagrant
        echo "Docker installed successfully"
      fi
      
      if [ "`which docker-compose`" == "" ]; then
        echo "Installing Docker Compose"
        curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-Linux-x86_64 > /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        echo "Docker Compose installed successfully"
      fi
    SHELL
  end

  config.vm.provision "shell" do |s|
    s.name = "Spin up Dockerized web environment"
    s.inline = <<-SHELL
      set -e
      
      project_dir="${1}"
      
      echo "Running composer install on the project directory"
      cd "$project_dir"
      docker-compose up -d
    SHELL
            
    s.args = [
      project_directory
    ] 
  end
end
