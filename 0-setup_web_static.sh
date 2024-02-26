#!/usr/bin/env bash
# A script to prepare a web server for deployment

# sudo apt-get update -y
# sudo apt-get upgrade -y
sudo apt install nginx -y


d1="/data/"
d2="/data/web_static"
d3="/data/web_static/releases"
d4="/data/web_static/shared"
d5="/data/web_static/releases/test"

if [ ! -d "$d1" ];then
	sudo mkdir -p "$d1"
fi
if [ ! -d "$d2" ]; then
	sudo mkdir -p "$d2"
fi
if [ ! -d "$d3" ]; then
	sudo mkdir -p "$d3"
fi
if [ ! -d "$d4" ]; then
	sudo mkdir -p "$d4"
fi
if [ ! -d "$d5" ]; then
	sudo mkdir -p "$d5"
fi


sudo touch /data/web_static/releases/test/index.html
echo "test index file" > sudo tee /data/web_static/releases/test/index.html

# Create Symbolic Link Here
web_static_path="/data/web_static"
releases_path="$web_static_path/releases/test"
current_path="$web_static_path/current"


if [ -L "$current_path" ]; then
	sudo rm "$current_path"
fi

# create a new symbolic link
sudo ln -s "$releases_path" "$current_path"

# Create Symbolic link here


# ~~~~ Change ownership of the /data/ folder and it's subfolders
data_path="/data"

sudo chown -R ubuntu:ubuntu "$data_path"

# ~~~~ Change ownership of folder


# ~~~ Configure nginx to serve the content of /data/web_static/current
# ~~~ to '/hbnb_static' endpoint.

nginx_config_location="/etc/nginx/sites-available/default"

regexp="location \/ {"
new_data="location \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n\t&"
sudo sed -i "0,/$regexp/s//$new_data/" $nginx_config_location

sudo nginx -s reload

# ~~~~ Configure nginx
