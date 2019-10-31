#!/bin/bash
python sparkMasterCreate.py
python sparkWorkerCreate.py
echo "starting spark deployement in 5 seconds"
sleep 5
ansible-playbook acc_project_QTLaas/spark_deployment.yml 
