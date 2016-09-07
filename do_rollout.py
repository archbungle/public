#Python code to build a basic droplet using D.O API
#And do basic lifecycle management of the droplet
#traiano, 31 August 2016
import digitalocean
import os

#User customised variables below (ADD YOUR D.O Account and ssh key here)
my_token="replace with your own DO API token"
hosts=[]
hosts_file="/Users/traianow/Projects/DO/hosts.orig"		#the ansible hosts file
private_key="/Users/traianow/Projects/DO/do_rsa"
wordpress_playbook="/Users/traianow/Projects/DO/wp_playbook.yml"
my_sshkey_id=3189478			#replace with your own D.O ssh key ID!

def operations_menu():
 status=0
 while(status != 15):
  print "1] Enter 1 for a list of droplets."
  print "2] Enter 2 to poweroff all droplets."
  print "3] Enter 3 startup all droplets."
  print "4] Enter 4 delete all droplets."
  print "5] Enter 5 to create a droplet"
  print "6] Enter 6 to get droplet details"
  print "7] Enter 7 to Ansible ping servers"
  print "8] Enter 8 to run wordpress playbook"
  print "9] Enter 9 to list D.O SSH keys"
  print "10] Enter 10 to update WordPress site"
  print "11] Enter 11 to restart Web Services"
  print "12] Enter 12 to generate Ansible hosts file."
  print "15] Enter 15 to quit."
  option=int(raw_input("option> "))
  if(option==1):
   list_all_droplets()
  elif(option==2):
   shutdown_droplets()
  elif(option==3):
   startup_droplets()
  elif(option==4):
   remove_all_droplets()
  elif(option==5):
   d_name=str(raw_input("Enter droplet name: "))
   d_name.strip("_")				# for anyone tempted to use underscores
   build_new_droplet(d_name) 
  elif(option==6):
   d_name=str(raw_input("Enter droplet name: "))
   d_name.strip("_")				# for anyone tempted to use underscores
   get_droplet_details(d_name)
  elif(option==7):
   ansible_ping_all() 
  elif(option==8):
   d_name=str(raw_input("Enter droplet name: "))
   d_name.strip("_")				# for anyone tempted to use underscores
   deploy_wp_playbook(d_name)
  elif(option==9):
   list_do_ssh_keys()
  elif(option==10):
   d_name=str(raw_input("Enter droplet name: "))
   d_name.strip("_")				# for anyone tempted to use underscores
   update_wp_code(d_name)
  elif(option==11):
   d_name=str(raw_input("Enter droplet name: "))
   d_name.strip("_")				# for anyone tempted to use underscores
   restart_web_services(d_name)
  elif(option==12):
   write_ansible_hosts_file()
  elif(option==15):
   status=15
   continue
  else:
   print "invalid option"

def write_ansible_hosts_file():
 manager = digitalocean.Manager(token=my_token)
 print ""
 print "Generating ansible hosts list."
 print ""
 droplets = manager.get_all_droplets()
 print ""
 for droplet in droplets:
   droplet_data=droplet.load()
   hosts.append(droplet_data.ip_address)
 print ""

 ansible_hosts_file=open(hosts_file,"w")
 for host in hosts:
  print "-> ",host
  ansible_hosts_file.write(host)
 print "Done with ansible hosts list."
 print ""

def restart_web_services(d_name):
 #restart web services on the specified web server
 print ""

def update_wp_code(d_name):
 #checkout latest WP site from GIT/Hub and ansible update the web servers
 print ""

def list_do_ssh_keys():
 manager = digitalocean.Manager(token=my_token)
 ssh_keys=manager.get_all_sshkeys()
 print ""
 for key in ssh_keys:
  print "ssh key: ",key
 print ""

def  deploy_wp_playbook(d_name):
 #deploy wordpress application on specified server
 print ""
 print "Running WordPress Server Playbook ..."
 print ""
 ansible_playbook_command="ansible-playbook --private-key "+private_key+" -u root -s "+wordpress_playbook+" -i "+"/Users/traianow/Projects/DO/hosts.orig"
 os.system(ansible_playbook_command)

def ansible_ping_all(): 
 #ansible ping all servers
 print ""
 print "Ansible pinging hosts in inventory: "
 ansible_ping_command="ansible -u root -i "+hosts_file+" --private-key="+private_key+" all -m ping"
 print ""
 print "Pinging with: ",ansible_ping_command
 print ""
 os.system(ansible_ping_command)

def get_droplet_details(d_name):
 #get details of a droplet
 manager = digitalocean.Manager(token=my_token)
 droplets = manager.get_all_droplets()
 print ""
 for droplet in droplets:
  if(droplet.name == d_name):
   droplet_data=droplet.load()
   print "droplet: ",d_name," network data: ",droplet_data.ip_address
 print ""

def build_new_droplet(d_name):
 print ""
 print "Building a new droplet ..."
 print ""
 droplet = digitalocean.Droplet(token=my_token,
 name=d_name,
 region='nyc2', 
 image='ubuntu-14-04-x64', 
 size_slug='512mb', 
 ssh_keys=[my_sshkey_id],
 backups=True)
 results=droplet.create()
 print "droplet creation data> ",results

def check_droplet_status(droplet):
 actions = droplet.get_actions()
 for action in actions:
  action.load()
  print "droplet: ",droplet,"action: ",action," Action Status: ",action.status

def shutdown_droplets():
 manager = digitalocean.Manager(token=my_token)
 droplets = manager.get_all_droplets()
 for droplet in droplets:
  droplet.shutdown()
  print "Shutting down droplet: "
  print ""
  check_droplet_status(droplet)

def remove_all_droplets():
 manager = digitalocean.Manager(token=my_token)
 droplets = manager.get_all_droplets()
 for droplet in droplets:
  droplet.destroy()
  check_droplet_status(droplet)

def list_all_droplets():
 manager=digitalocean.Manager(token=my_token)
 droplets=manager.get_all_droplets()
 for droplet in droplets:
  print "droplet: ",droplet

def startup_droplets():
 manager = digitalocean.Manager(token=my_token)
 droplets = manager.get_all_droplets()
 for droplet in droplets:
  droplet.power_on()
  check_droplet_status(droplet)
 
def shutdown_droplets():
 manager = digitalocean.Manager(token=my_token)
 droplets = manager.get_all_droplets()
 for droplet in droplets:
  droplet.shutdown()
  check_droplet_status(droplet)

operations_menu()
