sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose;
sudo chmod +x /usr/local/bin/docker-compose;
docker-compose --version;
if [$MODE == 'geckodriver']; then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz;
    tar -xzf geckodriver-*.tar.gz;
    chmod +x geckodriver;
    cp geckodriver /usr/local/bin/;
    cd ~;
    wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/89.0/linux-x86_64/zh-CN/firefox-89.0.tar.bz2;
    tar -jxf firefox-*.tar.bz2;
    mv firefox /opt;
    ln -s /opt/firefox/firefox /usr/local/bin/firefox;
    firefox --version;
elif [$MODE == 'chromedriver']; then
    wget http://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip;
    unzip chromedriver_linux64.zip
    chmod +x chromedriver;
    cp chromedriver /usr/local/bin/;
    cd ~;
    wget https://dl.google.com/linux/deb/pool/main/g/google-chrome-stable/google-chrome-stable_98.0.4758.102-1_amd64.deb
    sudo dpkg -i google-chrome*;
    sudo apt-get -f install
    sudo apt-get install google-chrome*;
    chrome --version;
else
    echo 'pass'
fi