# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.exceptions import Warning


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_date = fields.Datetime(comodel_name='sale.order', string='Sale Date',
                                related='order_id.date_order', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):

        # sale_order = self.env['sale.order'].search([('parnter_id','=',self.order_id.partner_id.id)])
        sales_line = self.env['sale.order.line'].search([('product_id','=',self.product_id.id ),('order_id.partner_id','=',self.order_id.partner_id.id)],order='create_date desc',limit=1)
        print(sales_line.price_unit)
        self.price_unit =  12

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        sales_line = self.env['sale.order.line'].search([('product_id','=',self.product_id.id ),('order_id.partner_id','=',self.order_id.partner_id.id)],order='create_date desc',limit=1)
        if sales_line :
            self.price_unit =  sales_line.price_unit


        elif self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)

