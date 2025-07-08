import os

def directory():
    dir_ask = input("Does a directory already exist for this application (Y/N)?: ")
    if dir_ask.upper() == "Y":
        global dir_location
        dir_location = input("Please enter the full path to the application's existing directory (/example/directory): ")
    elif dir_ask.upper() == "N":
        dir_base = input("Please enter the base directory for your containers (/example): ")
        dir_new = input("Please name the new directory you'd like to hold this application's data in (/example): ")
        os.system(f"mkdir {dir_base}{dir_new}")
        global created_dir
        created_dir = (f"{dir_base}{dir_new}")
    else:
        print("Please enter a valid option.")
        directory()

def compose():
    global compose_ask
    compose_ask = input("Will you be deploying this container with an already locally existing docker-compose.yml file (Y/N)?: ")
    if compose_ask.upper() == "Y":
        input("Please place your existing compose file into the container's directory and then press enter.")
    elif compose_ask.upper() == "N":
        global compose_url
        compose_url = input("Please enter the URL to your compose file: ")
        os.system(f"cd {created_dir} && wget -q {compose_url}")
    else:
        print("Please enter a valid option.")
        compose()

def deploy():
    compose_file = input("Please enter the name and extension of your compose file (ex: docker-compose.yml): ")
    if compose_ask.upper() == "Y":
        os.system(f"cd {dir_location} && docker-compose -f {compose_file} up -d")
    elif compose_ask.upper() == "N":
        os.system(f"cd {created_dir} && wget -q {compose_url} && docker-compose -f {compose_file} up -d")
    else:
        print("Please enter a valid option.")
        deploy()

directory()
compose()
deploy()