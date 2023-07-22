from pony import orm
from entities.seller import def_seller_entity
from entities.sales import def_sales_entity


db = orm.Database()
# db.bind(provider='postgres', user='', password='', host='', database='')
db.bind(provider='sqlite', filename="SUBSCRIPTION.db", create_db=True)
sellersEntity = def_seller_entity(db, orm)
salesEntity = def_sales_entity(db, orm, sellersEntity)
db.generate_mapping(create_tables=True)