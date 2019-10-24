#!/bin/bash
./ansible_install.sh
echo "130.238.28.88 15ansible" >> /etc/hosts
echo "130.238.28.95 15sparkmaster" >> /etc/hosts
echo "130.238.28.158 15sparkworker" >> /etc/hosts
echo "[sparkmaster]" >> /etc/ansible/hosts
echo "15sparkmaster" >> /etc/ansible/hosts
echo "[sparkworker]" >> /etc/ansible/hosts
echo "15sparkworker" >> /etc/ansible/hosts
python sparkmaster.py
python sparkworker.py
ansible-playbook -b spark_deployment.yml
