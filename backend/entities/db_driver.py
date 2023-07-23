
from pony.orm import set_sql_debug, Database
from entities.seller import def_seller_entity
from entities.sales import def_sales_entity


db = Database()
# set_sql_debug(True)
db.bind(provider='sqlite', filename="SUBSCRIPTION.db", create_db=True)
sellersEntity = def_seller_entity(db)
salesEntity = def_sales_entity(db, sellersEntity)
db.generate_mapping(create_tables=True)
