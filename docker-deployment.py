import os
import time
import requests
import sys

get_compose_file = None
input_port_check = None
existing_dir_check = None
exisiting_dir_location = None
base_dir_name = None
new_dir_name = None

def dir_check():
    global existing_dir_check
    existing_dir_check = input("Does a directory already exist for this application (Y/N)?: ")
    if existing_dir_check.upper() == ("Y"):
        global exisiting_dir_location
        exisiting_dir_location = input("Please enter the application directory/location (/example/path): ")
    elif existing_dir_check.upper() == ("N"):
        create_dir()
    else:
        print("Please enter a valid option.")
        dir_check()

def create_dir():
    global base_dir_name
    base_dir_name = input("Please enter the base directory for your containers (/example): ")
    global new_dir_name
    new_dir_name = input("Please enter a name for the new directory (/example): ")
    dir_create = os.system(f"cd {base_dir_name} && sudo mkdir {base_dir_name}{new_dir_name}")
    if dir_create == 0:
        print("Successfully created application directory.")
    elif dir_create > 0:
        print("Failed to create application directory.")
        sys.exit()
        

def docker_deployment():
    get_compose_file = input("Please enter the URL to your docker-compose.yml file: ")
    compose_file_name = input("Please enter the full name and extension of your docker-compose.yml file: ")
    compose_exist_check = f"{exisiting_dir_location}/{compose_file_name}"
    compose_newdir_check = f"{base_dir_name}/{new_dir_name}/{compose_file_name}"
    if existing_dir_check.upper() == ("Y"):
        os.system(f"cd {exisiting_dir_location} && wget -q {get_compose_file}")
        if os.path.exists(exisiting_dir_location):
            print("The provided docker-compose.yml file has been placed in the specified directory.")
            input_port_check = input("Please enter the web interface port of the application being deployed: ")
            cont_start = os.system(f"cd {exisiting_dir_location} && sudo docker-compose -f {compose_file_name} up -d")
        if cont_start == 0:
            print("Waiting for container to initialise...")
            time.sleep(5)
            get_http_status = requests.get(f"http://127.0.0.1:{input_port_check}")
            print("Your application returned an HTTP status code of", get_http_status.status_code)
    elif existing_dir_check.upper() == ("N"):
        os.system(f"cd {base_dir_name}{new_dir_name} && wget -q {get_compose_file}")
        if os.path.exists(compose_newdir_check):
            print("The provided docker-compose.yml file has been placed in the specified directory.")
            input_port_check = input("Please enter the web interface port of the application being deployed: ")
            cont_start = os.system(f"cd {base_dir_name}{new_dir_name} && sudo docker-compose -f {compose_file_name} up -d")
        
        #This has been commented out as I found it has pretty ugly stack trace errors if the request fails to reach the site
        #Docker informs you on whether the container deployed or not so I feel this is somewhat unnecessary for now
        
        #if cont_start == 0:
            #os.system(f"sudo docker ps")
            #print("Waiting for container to initialise...")
            #time.sleep(1)
            #get_http_status = requests.get(f"http://127.0.0.1:{input_port_check}")
            #print("Your application returned an HTTP status code of", get_http_status.status_code)###

dir_check()
docker_deployment()
