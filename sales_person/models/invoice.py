from odoo import api, fields, models

class invoice(models.Model):
    _inherit = 'account.move'

    sales_person = fields.Many2one(comodel_name="res.partner", string="Sales Person", required=False, )

