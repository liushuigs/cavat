#cavat project init

## set up crawler
make sure you are in PROJECT/crawler folder
### install dependencies
set up virtualenv

```
virtualenv env && source env/bin/activate
```

install dependencies

```
pip install -r requirements.txt
```
### init database
```
copy alembic.ini.example alembic.ini
copy configs/dev.config.example.ini configs/dev.config.ini
```

change the sqlalchemy.url to your own

init database
```
alembic upgrade head
```

### run crawler

```
scrapy crawl 36kr
```
