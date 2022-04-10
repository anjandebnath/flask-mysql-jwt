### Mysql on windows
1. Go to ``C:\Program Files\MySQL\MySQL Server 8.0\bin``
and run `cmd`
2. Now to connect to Mysql server write this command ``mysql -u root -p``
3. Then Enter password

### Create Flask project inside pycharm and JWT token
https://medium.com/@mushtaque87/flask-in-pycharm-community-edition-c0f68400d91e
1. inside terminal run `` pip install -r requirements.txt``
2. To create signature JWT write ``python`` inside terminal
3. Then write `` import os`` & ``os.urandom(12)``
4. ``\xee[\xdc\x15\x88\xe8\xdf\xac\x85\xb4\x87\x16``

#### to get jwt token run this ``http://localhost:5000/``

#### MYSQL connector 
SQLAlchemy already supports mysql and other dtabases driver.
Simply install ``mysql-connector``, ``mysql-connector-python`` drivers
through pip install.
1. Also, install ``PyMysql`` and ``Cryptography`` in the venv.
2. then in terminal run ``python`` and Create Table through:
3. ```from app import db```
4. ```db.create_all()```
5. Insert Data
6. ``from app import Product``
7. `` p1 = Product('Siesta Key Water','2 Bedrooms \u00b7 2 Bathrooms'
,'https://media.c6.jpg',185)``
8. `db.session.add(p1)`
9. ``db.session.commit()``
10. Query the Property
11. ``product = Product.query.all()``
12. ``for p in product:``
    1.      ``print(p.propertyTitle)`` 

important reference: 
1. https://www.youtube.com/watch?v=hQl2wyJvK5k
2. https://www.codestudyblog.com/cnb08/0818093912.html
3. https://dev.to/blankgodd/connecting-to-a-mysql-database-with-sqlalchemy-lmc


### GET request to get the properties from database
https://www.nintyzeros.com/2019/11/flask-mysql-crud-restful-api.html
Create a RESTful api using Flask and document it by generating API specification using openapi
Now Running below url
``http://localhost:5000/property``

Output is 
``{
  "product": [
    {
      "id": 1, 
      "propertyBrand": "https://media.c6.jpg", 
      "propertyDescription": "2 Bedrooms \u00b7 2 Bathrooms", 
      "propertyPrice": 185, 
      "propertyTitle": "Siesta Key Water"
    }, 
    {
      "id": 2, 
      "propertyBrand": "https://media.c7.jpg", 
      "propertyDescription": "Sleeps 2 Studio 1 Bathroom", 
      "propertyPrice": 222, 
      "propertyTitle": "Ground Floor Direct"
    }
  ]
}``

#### Get request to get response from database and Openapi standard

``http://localhost:5000/api/swagger.json``

Output is 

``{
  "info": {
    "title": "flask-api-swagger-doc", 
    "version": "1.0.0"
  }, 
  "openapi": "3.0.2", 
  "paths": {
    "/property": {
      "get": {
        "description": "Get List of Properties", 
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/VrboPropertyResponseSchema"
                }
              }
            }, 
            "description": "Return a Property list"
          }
        }
      }
    }
  }
}``


#### Get swagger UI run 

``http://localhost:5000/docs``


