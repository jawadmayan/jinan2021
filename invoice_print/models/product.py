from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partno = fields.Char(string="Part No.", required=False, )
