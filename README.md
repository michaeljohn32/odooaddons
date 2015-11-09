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

"mrp_send_to_production"
====================
This addon makes an extra stage in the manufacturing process
to confirm that the MO was "sent to production" 

This is useful when we need an extra confirmation step
that the work order/manufacturing order is in the production
department's hands

"stock_location_transfer_stock"
====================
This addon adds an option to the "More" dropdown of the "Locations"
view in the warehouse that allows you transfer all unreserved stock 
from one internal location to another.

