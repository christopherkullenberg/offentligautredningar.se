# offentligautredningar.se
Scripts for building [offentligautrednignar.se]{offentligautredningar.se}



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
