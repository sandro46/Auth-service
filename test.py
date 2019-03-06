import jwt, sys, os, uuid, json
from flask import jsonify
from models import Product, Prod_cat, Prod_component, Prod_component_rel
from app import db, to_json, sql_to_dict


# prodComponen_agg = func.array_agg(Prod_component.id, type_=ARRAY(Integer)).label('prod_components')
product = db.session.execute('''
	SELECT
		p.*,
		cat.name category,
        to_char(p.created, 'dd.mm.yyyy') created,
        to_char(p.modif, 'dd.mm.yyyy') modif,
		prod_comp.list components_list
	FROM app.product p
	left join app.prod_cat cat ON cat.id=p.cat
	left join (
		SELECT
			 cr.product_id,
			array_agg(cr.component_id) list
		from app.prod_component_rel cr
		group by cr.product_id
	) prod_comp ON prod_comp.product_id=p.id
''')

res = json.dumps([dict(row) for row in product])
print(res)
