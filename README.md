# Charybdis

## Installation & Setup

Requires Python3.5.


### Clone repository
```
$ sudo git clone git@github.com:acaceres2176/charybdis.git
```

### Java 8
Install:

```
$ sudo add-apt-repository ppa:webupd8team/java
```

```
sudo apt-get update
```

```
sudo apt-get install oracle-java8-installer
```

### Solr

Install:
```
$ cd PROJECT_DIR
$ mkdir solr
$ curl -LO https://archive.apache.org/dist/lucene/solr/6.6.0/solr-6.6.0.tgz
$ tar -C solr -xf solr-6.6.0.tgz --strip-components=1
$ sudo ./solr/bin/install_solr_service.sh solr-6.6.0.tgz
$ sudo chown -R solr:solr /var/solr/
```

### Python dependencies

```
$ pip install -r requirements.txt
```

```
$ sudo apt-get install python-software-properties
```

### Initialize the app database
```
$ ./manage.py migrate
$ ./manage.py collectstatic
```

### Start the app
Set environment variables:
```
$ export STRIPE_TEST_PUBLIC_KEY=your_test_public_key
$ export STRIPE_TEST_SECRET_KEY=your_test_secret_key
$ export STRIPE_LIVE_PUBLIC_KEY=your_live_public_key
$ export STRIPE_LIVE_SECRET_KEY=your_live_secret_key
```

Start Solr:

```
$ ./manage.py startsolr
```

Create the collection:

```
$ sudo su - solr -c "/opt/solr/bin/solr create -c credentials -n data_driven_schema_configs"
```

Run development server:
```
$ ./manage.py runserver
```
The app should now be available on port 8000.

## Production Deployment

### Create logs
```
$ sudo mkdir /var/log/charybdis
$ sudo touch /var/log/charybdis/uwsgi.log
$ sudo chmod 644 /var/log/charybdis/uwsgi.log
% sudo chown -R charybdis:charybdis /var/log/charybdis
```


