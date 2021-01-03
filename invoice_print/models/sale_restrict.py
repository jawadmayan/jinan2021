from odoo import api, fields, models
from odoo.exceptions import Warning as UserError


class NewModule(models.Model):
    _inherit = 'sale.order.line'

    # @api.onchange('product_uom_qty', 'product_id')
    # def low_stock_check(self):
    #     if self.product_id:
    #         if self.product_id.product_type == 'product':
    #             stocks = []
    #             warehouse = self.warehouse_id
    #             stock_in_location = []
    #             availables_stock = []
    #
    #             for quantity in self:
    #                 stocks = self.env['stock.quant'].search([
    #                     ('product_id', '=', quantity.product_id.id),
    #                     ('location_id.usage', '=', 'internal'),
    #                     ('company_id', '=', quantity.order_id.company_id.id)
    #                 ])
    #
    #             for entry in stocks:
    #                 if entry.location_id == warehouse.lot_stock_id:
    #                     stock_in_location = entry
    #                 else:
    #                     availables_stock.append(entry)
    #             other_location = ''
    #             for a_stock in availables_stock:
    #                 warehouse_name = self.env['stock.warehouse'].search([('lot_stock_id', '=', a_stock.location_id.id)])
    #                 other_location += '\n ' + warehouse_name[0].name + "  " + str(a_stock.quantity) + '\n'
    #
    #             if stock_in_location:
    #                 if stock_in_location[0].quantity < self.product_uom_qty:
    #                     raise UserError('Available stock in \n\n' + str(warehouse.name) + ' ' + str(
    #                         stock_in_location[0].quantity) + other_location)
    #             else:
    #                 raise UserError('Available stock in \n\n' + str(warehouse.name) + ' ' + (
    #                     stock_in_location[0].quantity if stock_in_location else '0' + other_location))
