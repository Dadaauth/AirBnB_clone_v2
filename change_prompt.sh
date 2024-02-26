#!/usr/bin/env bash

echo -e "# Personal Modification\n" >> ~/.bashrc
echo -e "$1" >> ~/.bashrc
echo -e "# Personal Modification End\n" >> ~/.bashrc

PS1=$1
