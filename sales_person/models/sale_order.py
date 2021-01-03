from odoo import api, fields, models

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    sales_person = fields.Many2one(comodel_name="res.partner", string="Sales Person", required=False, )

    def _prepare_invoice(self):
        invoice_vals = super(SalesOrder, self)._prepare_invoice()

        if self.sales_person:
            invoice_vals['sales_person'] = self.sales_person.id
        return invoice_vals


class SaleReport(models.Model):
    _inherit = 'sale.report'

    sales_person = fields.Many2one(comodel_name="res.partner", string="Sales Person", required=False, )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['sales_person'] = ", s.sales_person as sales_person"
        groupby += ', s.sales_person'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)