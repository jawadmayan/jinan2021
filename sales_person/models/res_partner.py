# -*- coding: utf-8 -*-
from odoo import api, fields, models



class NewModule(models.Model):

    _inherit = 'res.partner'

    is_seles_person = fields.Boolean(string="Sales Person",  )
