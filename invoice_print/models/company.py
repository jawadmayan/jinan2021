from odoo import api, fields, models

class CompanyInherit(models.Model):
    _inherit = 'res.company'


    bank_name = fields.Char(string="Bank", required=False, )
    acc_no = fields.Char(string="Account No", required=False, )
    ifsc = fields.Char(string="IFS Code", required=False, )
    branch = fields.Char(string="Branch", required=False, )

