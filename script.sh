#!/bin/bash
./ansible_install.sh
sudo echo "130.238.28.115 group-15-ansible" >> /etc/hosts
sudo echo "130.238.28.100 15sparkmaster" >> /etc/hosts
sudo echo "130.238.28.134 15sparkworker" >> /etc/hosts
sudo echo "[sparkmaster]" >> /etc/ansible/hosts
sudo echo "group-15-sparkmaster" >> /etc/ansible/hosts
sudo echo "[sparkworker]" >> /etc/ansible/hosts
sudo echo "group-15-sparkworker" >> /etc/ansible/hosts
python sparkmaster.py
python sparkworker.py
ansible-playbook -b spark_deployment.yml
