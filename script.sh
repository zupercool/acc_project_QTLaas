#!/bin/bash
./ansible_install.sh
echo "192.168.1.72 15ansible" >> /etc/hosts
echo "192.168.1.74 15sparkmaster" >> /etc/hosts
echo "192.168.1.62 15sparkworker" >> /etc/hosts
echo "15sparkmaster ansible_ssh_host=192.168.1.74" >> /etc/ansible/hosts
echo "15sparkworker ansible_ssh_host=192.168.1.62" >> /etc/ansible/hosts
echo "[sparkmaster]" >> /etc/ansible/hosts
echo "15sparkmaster ansible_connection=local ansible_user=ubuntu" >> /etc/ansible/hosts
echo "[sparkworker]" >> /etc/ansible/hosts
echo "15sparkworker ansible_connection=local ansible_user=ubuntu" >> /etc/ansible/hosts
echo "[sparkmaster]" >> /etc/ansible/hosts
echo "15sparkmaster" >> /etc/ansible/hosts
echo "[sparkworker]" >> /etc/ansible/hosts
echo "15sparkworker" >> /etc/ansible/hosts
python sparkmaster.py
python sparkworker.py
ansible-playbook -b spark_deployment.yml
