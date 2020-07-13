require 'yaml'
conf = YAML.load_file("vagrant_conf.yaml")

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.network "forwarded_port", guest: 7071, host: 7071
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end

  config.vm.provision "shell", args: ["#{conf['root_db_passwd']}", "#{conf['default_user']}", "#{conf['default_passwd']}"],inline: <<-SHELL
    sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt install curl -y && sudo apt install net-tools -y
    sudo -u vagrant \
    sudo curl -s https://cairis.org/quickInstall.sh | bash -s -- $1 $2 $3
  SHELL
end
