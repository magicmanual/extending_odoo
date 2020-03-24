from collections import namedtuple, OrderedDict, defaultdict
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import split_every
from psycopg2 import OperationalError

from odoo import api, fields, models, registry, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round

from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class StockRule (models.Model):
    _inherit = 'stock.rule'




    @api.model
    def _run_pull(self, procurements):
        moves_values_by_company = defaultdict(list)
        mtso_products_by_locations = defaultdict(list)

        # To handle the `mts_else_mto` procure method, we do a preliminary loop to
        # isolate the products we would need to read the forecasted quantity,
        # in order to to batch the read. We also make a sanitary check on the
        # `location_src_id` field.
        for procurement, rule in procurements:
            if not rule.location_src_id:
                msg = _('No source location defined on stock rule: %s!') % (rule.name, )
                raise UserError(msg)

            if rule.procure_method == 'mts_else_mto':
                mtso_products_by_locations[rule.location_src_id].append(procurement.product_id.id)

        # Get the forecasted quantity for the `mts_else_mto` procurement.
        forecasted_qties_by_loc = {}
        for location, product_ids in mtso_products_by_locations.items():
            products = self.env['product.product'].browse(product_ids).with_context(location=location.id)
            forecasted_qties_by_loc[location] = {product.id: product.virtual_available for product in products}

        # Prepare the move values, adapt the `procure_method` if needed.
        for procurement, rule in procurements:
            procure_method = rule.procure_method
            if rule.procure_method == 'mts_else_mto':
                qty_needed = procurement.product_uom._compute_quantity(procurement.product_qty, procurement.product_id.uom_id)
                qty_available = forecasted_qties_by_loc[rule.location_src_id][procurement.product_id.id]
                if float_compare(qty_needed, qty_available, precision_rounding=procurement.product_id.uom_id.rounding) <= 0:
                    procure_method = 'make_to_stock'
                    forecasted_qties_by_loc[rule.location_src_id][procurement.product_id.id] -= qty_needed
                else:
                    procure_method = 'make_to_order'

            move_values = rule._get_stock_move_values(*procurement)
            move_values['procure_method'] = procure_method
            moves_values_by_company[procurement.company_id.id].append(move_values)

        for company_id, moves_values in moves_values_by_company.items():
            print('before')
            print(moves_values)
            #move_values=list(filter(self.is_mask_product,list(move_values)))
            moves_values=list(filter(lambda move_single:self.env['sale.order.line'].browse(move_single['sale_line_id']).is_mask_product==False,moves_values))
            print('after')
            print(moves_values)


            # create the move as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
            moves = self.env['stock.move'].sudo().with_context(force_company=company_id).create(moves_values)
            # Since action_confirm launch following procurement_group we should activate it.
            moves._action_confirm()
        return True



