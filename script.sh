#!/bin/bash
./ansible_install.sh
echo "130.238.28.115 group-15-ansible" >> /etc/hosts
echo "130.238.28.103 15sparkmaster" >> /etc/hosts
echo "130.238.28.135 15sparkworker" >> /etc/hosts
echo "[sparkmaster]" >> /etc/ansible/hosts
echo "15sparkmaster" >> /etc/ansible/hosts
echo "[sparkworker]" >> /etc/ansible/hosts
echo "15sparkworker" >> /etc/ansible/hosts
python sparkmaster.py
python sparkworker.py
ansible-playbook -b spark_deployment.yml
