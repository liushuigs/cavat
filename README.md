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
```

change the sqlalchemy.url to your own

init database
```
alembic upgrade head
```

### run crawler

run crawler and it will create 5045706.html
```
scrapy crawl 36kr
```

run test, you'll see the parsed result
```
python test/test_a36kr.py
```