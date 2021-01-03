# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceDataExtent(models.Model):
    _inherit = 'account.move'

    sale_order = fields.Many2one(comodel_name="sale.order", string="Sale Order", required=False,
                                 compute="_compute_sale_order", store=True)
    po_number = fields.Char(string="PO Number", required=False, related="sale_order.po_number")
    invoice_template = fields.Selection(string="Template",
                                        selection=[('1', 'Template 1'), ('2', 'Template 2'), ('3', 'Template 3'), ],
                                        required=False, )
    # store_no = fields.Char(string="Store No", required=False, related="sale_order.store_no")
    ref = fields.Char(string='Reference', copy=False, related="sale_order.ref")
    store_no = fields.Many2one(
        'stock.warehouse', 'Store No',
        check_company=True, ondelete="cascade", related="sale_order.warehouse_id")

    grv_no = fields.Char(string="GRV Document No.", required=False, )
    other_ref = fields.Char(string="Other Reference(s)", required=False, )
    po_date = fields.Date(string="PO Dated", required=False, )
    dispatched_trough = fields.Char(string="Dispatched Trough", required=False, )
    destination = fields.Char(string="Destination", required=False, )
    terms_of_delivery = fields.Text(string="Terms of Delivery", required=False, )


    @api.depends('invoice_origin')
    def _compute_sale_order(self):
        for i in self:
            sale_order = i.env['sale.order'].search([('name', '=', i.invoice_origin)])
            if sale_order:
                i.sale_order = sale_order.id
            else:
                i.sale_order = False

    def package_list(self):
        for record in self :
            packages = {}
            packages_str = ''
            for lines in record.invoice_line_ids:
                if lines.product_packaging :
                    if lines.product_packaging.name in packages.keys():
                        packages[lines.product_packaging.name] = packages[lines.product_packaging.name].value()+lines.quantity / lines.product_packaging.qty
                    else :
                        packages[lines.product_packaging.name] = lines.quantity / lines.product_packaging.qty

            for i in packages :
                packages_str += str(int(packages[i])) +' '+ str(i) +'<br/>'
            print(packages_str)
            return packages_str


class SalOrderData(models.Model):
    _inherit = 'sale.order'

    po_number = fields.Char(string="PO Number", required=False, )
    # invoice_template = fields.Selection(string="Template", selection=[('1', 'Template 1'), ('2', 'Template 2'),('3', 'Template 3'), ], required=False, )
    store_no = fields.Char(string="Store No", required=False, )
    ref = fields.Char(string="Reference", required=False, )
    warehouse_id = fields.Many2one(
        'stock.warehouse', 'Store No',
        check_company=True, ondelete="cascade", required=True)

    grv_no = fields.Char(string="GRV Document No.", required=False, )
    other_ref = fields.Char(string="Other Reference(s)", required=False, )
    po_date = fields.Date(string="PO Dated", required=False, )
    dispatched_trough = fields.Char(string="Dispatched Trough", required=False, )
    destination = fields.Char(string="Destination", required=False, )
    terms_of_delivery = fields.Text(string="Terms of Delivery", required=False, )


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id :
            if self.partner_id.warehouse_id :
                self.warehouse_id = self.partner_id.warehouse_id

    def _prepare_invoice(self):
        invoice_vals = super(SalOrderData, self)._prepare_invoice()
        invoice_vals['grv_no'] = self.grv_no
        invoice_vals['other_ref'] = self.other_ref
        invoice_vals['po_date'] = self.po_date
        invoice_vals['dispatched_trough'] = self.dispatched_trough
        invoice_vals['destination'] = self.destination
        invoice_vals['terms_of_delivery'] = self.terms_of_delivery
        return invoice_vals

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()

        res = super(SaleOrderLineInherit, self)._prepare_invoice_line()
        if self.product_packaging:
            print("JJJJ")
            res['product_packaging'] = self.product_packaging.id
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_packaging = fields.Many2one(comodel_name="product.packaging", string="Package", required=False, )




class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    invoice_template = fields.Selection(string="Template",
                                        selection=[('1', 'Template 1'), ('2', 'Template 2'), ('3', 'Template 3'), ],
                                        required=False, )

    def send_and_print_action(self):
        invoice = self.env['account.move'].search([('id', '=', self.res_id)])
        invoice.write({"invoice_template": self.invoice_template})

        return super(AccountInvoiceSend, self).send_and_print_action()


class ResPartnerWithWarehouse(models.Model):
    _inherit = 'res.partner'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Default warehouse',
                                   ondelete="cascade")



class PONumber(models.Model):
    _inherit = 'sale.report'

    po_number = fields.Char(string="PO Number", required=False, )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['po_number'] = ", s.po_number as po_number"
        groupby += ', s.po_number'
        return super(PONumber, self)._query(with_clause, fields, groupby, from_clause)