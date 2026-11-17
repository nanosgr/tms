# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _prepare_asset_vals(self, aml):
        vals = super()._prepare_asset_vals(aml)
        if aml.asset_profile_id.is_vehicle:
            if not aml.product_id.model_id:
                raise ValidationError(
                    _(
                        "You are trying to create a TMS vehicle asset from a product. "
                        "Please set the vehicle model inside the product."
                    )
                )
            vals["model_id"] = aml.product_id.model_id.id
        return vals
