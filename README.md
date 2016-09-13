# offentligautredningar.se
Scripts and source data for building [offentligautrednignar.se](offentligautredningar.se). This database will contain
index of Statens Offentliga Utredningar based on the digitalised repository
made public by the National Library of Sweden.

The search engine is based on Apache Solr and relies on Python3 and cgi-bin
to create the dynamic front end.

**Note:** This project is a prototype and nothing more. Feel free to suggest improvements
and features.

Data and source code should be free, so here follows an instruction on how to
replicate offentligautredningar.se on your own machine(s).

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

Edit `/etc/apache2/apache2.conf` to add:

    <Directory /home/yourdirectory/offentligautredningar.se/>
         Options Indexes FollowSymLinks
         AllowOverride None
         Require all granted
    </Directory>

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

You should now be able to access the Solr admin interface at `yourhostname.com:8983`. **Warning:** Your machine is now exposed to the internet. Make sure you lock down your setup before proceeding and read up on Solr security.  

Increasing memory heap. The default configuration of Solr will crash unless you increase the memory heap.
The data is too large for the default 512Mb. Edit `/etc/decault/solr.in.sh` and change the heap size into `SOLR_HEAP="6g"`.




### Installing scripts, Python3 modules and static html

    git clone https://github.com/christopherkullenberg/offentligautredningar.se.git
    sudo pip3 install vincent pysolr


### Index files to Solr database
Create a new Solr core:

    sudo su - solr -c "/opt/solr/bin/solr create -c sou -n data_driven_schema_configs"

Enter the Solr admin interface on `yourhostname.com:8983`. Select the core you just created, then add the following to the Schema:


| Core name     | Type          |
| ------------- |:-------------:|
| year      | int|
| number    | int      |
| filename | string      |
| pdfurl | string	|
| fulltext | text_sv      |

Open up the script `SOUtoSolr.py`. Change the diretory structure to reflect where you stored the cache of text documents. **Note:** You have to change directory twice in the loop that reads the files from disk. **Note:** You must have `sqlite3` installed on your system to read the PDF urls. On ubuntu: `sudo apt-get install sqlite3`.

Indexing 8000+ files will probably take some time. Use for example `screen` to be able to resume if your ssh connection drops:

    screen python3 SOUtoSolr.py

Wait for the files to index. On the above mentioned setup it was done in ~2 hours.

### Bring up the web front

Ensure that the following files that were cloned from this Git repository
are present in the web root:

    cgi-bin/solrsearch.py  
    chart.html  
    index.html  
    indexPlain.html  
    results  
    searchicon.png  
    style.css

Edit the main script `solrsearch.py`and change the following line to reflect the
name of your Solr core:

    solr = pysolr.Solr('http://localhost:8983/solr/nameofyourcoure/', timeout=1000)

Make the script executable:

    chmod 755 /cgi-bin/solrsearch.py
