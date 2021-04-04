# menagerie-mysql-pd-demo
This is a crude Python demo program and Jupyter notebook used to demonstrate Pandas, MySQL interactions, etc. It can be a "jumping-off point" for further development, requirements gathering, etc.

## How Do I Use This Demo?

* **Clone this repository**: `git clone https://github.com/babalugats76/menagerie-mysql-pd-demo.git`
* **Install requirements** (optional): `pip install -r requirements.txt`
* **Create an `.env` file** in the cloned project directory of the following form:
```
MYSQL_HOST=xxxxxx.xxxxx.xxxxxx
MYSQL_PORT=3306
MYSQL_USER=xxxxx
MYSQL_PASSWORD=xxxxx
MYSQL_DATABASE=xxxxx
```
* Run `pets.ipynb` which basically just wraps a call to `%run pets.py` (alternatively, `python pets.py`)
* Review `pets.py` in detail

## Which MySQL Client Should I Use and When?

For this project, it would probably be best to use some combination of `SQLAlchemy` and/or `pymysql`. `SQLAlchemy` appears to be very tightly-coupled with `pandas` sql functionality.  I set up the demo to accommodate either; in the end, they are not mutually exclusive.  Which one you need (or both) is tied directly to what you will be doing and, in particular, which Pandas methods you will be employing in your solutions.

In most use cases, `SQLAlchemy` is used as an **ORM** (Object-Relational Mapping) tool which serves as a go-between-like translation layer between the database and object-oriented applications' object instances. Often you will see "duplicate" libaries due to: differences in the underlying language used, e.g., `C` vs. `Python`; whether they are synchronous or allow for asynchronous threading; and often because they target a specific framework, e.g., `Flask`.  Gross oversimplification, but that is the gist.

## How Do I Setup/Use Database Credential Configuration?

In the Python ecosystem, this is normally done with the uber-popular `python-dotenv`.  Basically, you setup a `.env` file with name/value pairs to be exported to your OS environment. Once exported to your environment, they can be referred to using variables via Python's built-in `os` module.  Follow the instructions and kick the tires on the demo to see it in action.

## How Do I Insert Data From a `dataframe` Into a MySQL Table?

Most commonly, [to_sql()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) is used to dump the contents of the `dataframe` into a database table.  I think this pretty much requires the use of `SQLAlchemy` but don't quote me on that.  There also appears to be a series of iteration methods, e.g., [iterrows()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html) that can be used to loop over the data, but the docs clearly say that modifications of these iterables is not safe.

If you end up needing to **merge** data, I would recommend doing that in the database, using SQL and some creative combination of DML/DDL.  Devil in the details on that one...

## How Should I Go About Handling Errors?

Depends on the nature of the process, how it will be run, how often, etc.  For starters, I would **functionize things**, similar to what I did in the demo, and make prodigious use of `try`-`except`-`finally` blocks.  Keeping things out of Jupyter might mean that you can write processes as all-encompassing single scripts whose error codes can be redirected and logged, etc. Devil in the details on this one too... 
