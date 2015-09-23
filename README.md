Odoo Addons
===========

This repository hosts a few different addons for use in odoo v.8


"mrp_bom_calculation"
====================
This addon calculates the "real" cost of a Bill of Materials within Odoo as
the item is produced using cost of each of the reserved quantities

When a user "consumes" a product, a boolean flag is set that that particular
move needs to be costed later

Finally, when a new item is "Produced":
- We add up the material cost of all subproducts
- Update the Product's cost with the value just obtained

"mrp_cancel_mo_line"
====================
This addon provides an easy way to cancel a manufacturing
order's line.  

Our usage is that if that particular line is not needed (ie
the bill of materials is wrong), we can mark it as cancelled
so the products are not reserved or required to produce a
particular bill of material.

"mrp_mto_with_stock"
====================
This addon makes a manufacturing order pull from stock
till the quantity is zero, and then generates a procurement

NOTE: this module depends on the OCA module: stock_mto_mts_rule


