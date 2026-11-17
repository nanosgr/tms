# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    tms_factor = fields.Float()
    tms_factor_uom = fields.Char(readonly=True)

    @api.depends("tms_factor")
    def _compute_totals(self):
        return super()._compute_totals()
