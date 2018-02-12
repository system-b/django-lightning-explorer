raito-lightning
===============

A lightning network explorer based on Django. [Demo](http://raito.systemb.co/).

# INSTALL and RUN
    git clone https://github.com/system-b/raito-lightning.git
    cd raito-lightning/
    virtualenv -p python3 .env
    source .env/bin/activate
    pip install -r requirements.txt
    vim backend/settings.py # change path to LIGHTNING_RPC and GEO_CITY_PATH for [geoip2-city](https://www.maxmind.com/en/geoip2-city)
    ./manage.py runserver 8080 
