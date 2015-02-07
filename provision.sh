#!/bin/bash

### speed up install

sudo add-apt-repository ppa:saiarcot895/myppa
sudo apt-get update
sudo apt-get -y install apt-fast

# install packages
sudo apt-get update
sudo apt-fast -y install language-pack-en build-essential git ruby ruby-dev make gcc nodejs
sudo gem install github-pages jekyll --no-ri --no-rdoc
