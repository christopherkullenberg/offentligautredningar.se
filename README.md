# offentligautredningar.se
Scripts for building [offentligautrednignar.se](offentligautredningar.se)



# Set up your own instance on Linux
Tested with with Ubutnu 14.04 LTS on a machine with 8 Gb of RAM and 4 CPU cores.

### Get the source data
    wget http://scientometrics.flov.gu.se/files/SOU19222015.zip
    unzip SOU19222015.zip

Note: The filenames contain Swedish characters `åäö`. Make sure your locale settings can handle it.

### Configuring a the web server (Apache2)

Make a web directory somewhere on your system that will serve as the document root.

    mkdir offentligautredningar.se
    mkdir offentligautredningar.se/results
    mkdir offentligautredningar.se/cgi-bin

Make the results directory writable:

    chmod -R +rw offentligautredningar.se/results/

Install Apache2 and and activate cgi-bin

    sudo apt-get install apache2
    sudo a2enmod cgi

Create a new configuration file in /etc/apache2/sites-available/ with the following configuration (change directories to your local settings):


    <VirtualHost offentligautredningar.se:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /home/username/offentligautredningar.se/
        ServerName offentligautredningar.se
        ServerAlias www.offentligautredningar.se

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        ScriptAlias /search /home/username/offentligautredningar.se/cgi-bin/solrsearch.py

        <Directory "/home/username/offentligautredningar.se/cgi-bin">
                AllowOverride None
                Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                Order allow,deny
                Allow from all
        </Directory>

    </VirtualHost>

Activate and reload Apache2:

    sudo a2ensite offentligautredningar.se.conf
    sudo service apache2 reload

### Installing Apache Solr 6
Install instructions inspired by [Techadmin](http://tecadmin.net/install-apache-solr-on-ubuntu/#):

    sudo apt-get update && apt-get upgrade -y
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java8-installer
    java -version
    cd /opt
    wget http://apache.mirror1.spango.com/lucene/solr/6.2.0/solr-6.2.0.tgz
    sudo tar xzf solr-6.2.0.tgz solr-6.2.0/bin/install_solr_service.sh --strip-components=2
    sudo bash ./install_solr_service.sh solr-6.2.0.tgz

You should now be able to access the Solr admin interface at `yourhostname.com:8983/solr/#/`. **Warning:** Your machine is now exposed to the internet. Make sure you lock down your setup before proceeding and read up on Solr security.  










### Installing scripts, Python3 modules and static html

    git clone https://github.com/christopherkullenberg/offentligautredningar.se.git
    sudo pip3 install 
