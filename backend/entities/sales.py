def def_sales_entity(db, orm, Sellers):
    class Sales(db.Entity):
        _table_ = 'sales'
        id = orm.PrimaryKey(int, auto=True)
        seller = orm.Required(Sellers, column='seller_id')
        price = orm.Required(int)
        item_name = orm.Optional(str, 40)
        date_time = orm.Required(str, 20)
    return Sales
