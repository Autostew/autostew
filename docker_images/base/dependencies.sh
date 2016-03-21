apt-get -y update
apt-get -y upgrade

apt-get -y install git vim zsh openssh-server
mkdir -p /var/run/sshd

# Set random password for the root user
echo "root:$(< /dev/urandom tr -dc A-Za-z0-9 | head -c 32)" | chpasswd

# add our ssh keys
mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3skDXkIY3kGbsvWRZGnbPOvH+IVTvkl5pWWCJpUqt04VGa+LGmN4O/qHe3Tehd5K6pspAr2xEs6xh/CBGJVCQ66sPQKIgxOuTuyELlf3Ix7o16CaCUUZKHTOdtx8au3Kr9KP2U4N4rLNKWMrsBfVp+wwWo9sVpOywjqG4APoQJzWnHE0Rfr7mHfPo1aRxr1hmu1Z2nz+sEtlLDvp9HXscEV3CB99H9ucK5QoiOxQglQbFUiLq3bjaEU9z2n4TNZxer0a68evDJMEqdzHrgHrqNooB+JYSWS1LB4QMACPI/cT6PWSYXwgKO+B5Sd8GBg80oOuSV8eRz9FhZD2FdD8z sh4ke@Beteigeuze" >> /root/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYyFgOZwK+IHB6fGplUJHIKEKtBagyuuaPLzF/RKNjDhTxvRkjcLIUXYrYkxj6iNfooo6ZQ0sI/yH4NWzKP64VrtWghOixDyQKXdqqf3IGTBPAuiNcOjIcFRdtxeqwtVBXZX7XpK75q0szlc8q0y7BLVr8a5ep1DcURPG/GKOV+tROWcswFBU/knAow40ZNzMnAc7hrwnYQDMGelsQOH9xWbziPQShjaL8xPk260AhqVxVkGqJOs1EnrTkq98bTYnzW5BBP+piD+ojFBDO9Ssma4Fje+56KACuNV+tLDYwQbdsM6afxAQqKKh59/pi7pOs6jpjCjEwCEIoA2vHHRbf joan" >> /root/.ssh/authorized_keys
