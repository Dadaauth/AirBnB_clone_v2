#!/usr/bin/env bash
# A script to prepare a web server for deployment
sudo apt-get update
sudo apt-get upgrade
sudo apt install nginx -y


d1="/data/"
d2="/data/web_static"
d3="/data/web_static/releases"
d4="/data/web_static/shared"
d5="/data/web_static/releases/test"

[ -d $d1 ] && sudo mkdir $d1;
[ -d $d2 ] && sudo mkdir $d2;
[ -d $d3 ] && sudo mkdir $d3;
[ -d $d4 ] && sudo mkdir $d4;
[ -d $d5 ] && sudo mkdir $d5;


sudo touch /data/web_static/releases/test/index.html
sudo echo "test index file" > /data/web_static/releases/test/index.html

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

# nginx_config_location="/etc/nginx/sites-available/default"

# nginx_config_update="location /hbnb_static/ {\n\talias /data/web_static/current/;\n}"

# sudo sed -i "/^\s*server \{/,/^\s*\}/ {/^\s*server \{/!{/^\s*\}/!{/$/!{N;s/\n/$nginx_config_update\n/}}}}" $nginx_config_location

# Define the path to the Nginx configuration file
nginx_config_location="/etc/nginx/sites-available/default"

# Define the alias and location in the Nginx configuration
nginx_config_update="location \/hbnb_static\/ {\\n\talias \/data\/web_static\/current\/;\\n}"

# Use sed to update the Nginx configuration file
sudo sed -i "/^\s*server {/,/^\s*}/ s@location / {@$nginx_config_update@" $nginx_config_location



sudo nginx -s reload

# ~~~~ Configure nginx
