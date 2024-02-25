#!/usr/bin/env bash
# A script to prepare a web server for deployment
sudo apt-get update
sudo apt-get upgrade
sudo apt install nginx -y
sudo mkdir /data/
sudo mkdir /data/web_static
sudo mkdir /data/web_static/releases
sudo mkdir /data/web_static/shared
sudo mkdir /data/web_static/releases/test
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

nginx_config_location="/etc/nginx/sites-available/default"

nginx_config_update="location /hbnb_static/ {\n\talias /data/web_static/current/;\n}"

sudo sed -i "/^\s*server \{/,/^\s*\}/ {/^\s*server \{/!{/^\s*\}/!{/$/!{N;s/\n/$nginx_config_update\n/}}}}" $nginx_config_location

sudo nginx -s reload

# ~~~~ Configure nginx
