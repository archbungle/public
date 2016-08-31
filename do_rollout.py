#Python code to build a basic droplet using D.O API
#And do basic lifecycle management of the droplet
#traiano, 31 August 2016
import digitalocean
my_token="your_personal_do_token"

def operations_menu():
 status=0
 while(status != 6):
  print "1] Enter 1 for a list of droplets."
  print "2] Enter 2 to poweroff all nodes."
  print "3] Enter 3 startup all nodes."
  print "4] Enter 4 delete all droplets."
  print "5] Enter 5 to create a droplet"
  print "6] Enter 6 to quit."
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
   status=6
   continue
  else:
   print "invalid option"

def build_new_droplet(d_name):
 droplet = digitalocean.Droplet(token=my_token,
 name=d_name,
 region='nyc2', 
 image='ubuntu-14-04-x64', 
 size_slug='512mb', 
 backups=True)
 droplet.create()

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
