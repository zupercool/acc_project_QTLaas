# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, syslog
import inspect
from os import environ as env
from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
import shade

hosts_file = '/etc/hosts'
ansible_hosts_file = '/etc/ansible/hosts'
flavor = "ssc.small" 
private_net = "SNIC 2019/10-32 Internal IPv4 Network" 
floating_ip_pool_name = None
floating_ip = "130.238.28.103"
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
instanceName='15sparkWorkerDummy'
loader = loading.get_plugin_loader('password')

if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

cloud = shade.openstack_cloud()   
'''ip=cloud.create_floating_ip()'''
ip=cloud.create_floating_ip('af006ff3-d68a-4722-a056-0f631c5a0039')
print ip

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default', 'vishnu','BootsmaSG']

instance = nova.servers.create(name=instanceName, image=image, flavor=flavor, userdata=userdata, nics=nics,security_groups=secgroups)
inst_status = instance.status
time.sleep(10)

while inst_status == 'BUILD':
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

server = cloud.get_server(instanceName)
cloud.add_ips_to_server(server, ips=ip['floating_ip_address'])

f = open("/etc/hosts", "a+")     #open file for reading
f.write('\n'+ip['floating_ip_address']+" "+instanceName)             #write the altered contents
f.close()

f = open(ansible_hosts_file, "a+")     #open file for reading
f.write('[sparkworker]\n')
f.write(instanceName+' ansible_connection=ssh ansible_user=ubuntu\n')    #write the contents
f.close()
