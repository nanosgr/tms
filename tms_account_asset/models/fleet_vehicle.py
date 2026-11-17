# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from markupsafe import Markup

from odoo import _, api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    asset_id = fields.Many2one("account.asset", string="Asset")
    asset_profile_id = fields.Many2one(related="model_id.category_id.asset_profile_id")
    actual_value = fields.Monetary(
        related="asset_id.value_residual", string="Asset Residual Value"
    )

    @api.model_create_multi
    def create(self, vals_list):
        vehicles = super().create(vals_list)
        if self.env.context.get("create_vehicle_from_asset"):
            return vehicles
        for vehicle in vehicles:
            if self.env["account.asset"].search_count(
                [("vehicle_id", "=", vehicle.id)]
            ):
                continue
            profile = vehicle.model_id.category_id.asset_profile_id
            if not profile:
                continue
            asset = (
                self.env["account.asset"]
                .with_context(create_from_vehicle=True)
                .create(
                    {
                        "name": f"VEHICLE - {vehicle.display_name}",
                        "purchase_value": 0.0,
                        "date_start": date.today(),
                        "profile_id": profile.id,
                        "vehicle_id": vehicle.id,
                        "model_id": vehicle.model_id.id,
                    }
                )
            )
            vehicle.asset_id = asset
            vehicle.message_post(
                body=_(
                    "An asset has been created for this vehicle: %s",
                    Markup(
                        '<a href="#" data-oe-model="account.asset" '
                        'data-oe-id="%s">%s</a>'
                    )
                    % (asset.id, asset.display_name),
                )
            )
        return vehicles

    def action_view_asset(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.asset",
            "view_mode": "form",
            "res_id": self.asset_id.id,
            "target": "current",
            "name": _("Asset for vehicle: %s", self.name),
        }
