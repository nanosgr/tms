# Copyright (C) 2024 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SeatTicket(models.Model):
    _name = "seat.ticket"
    _description = "Seat Ticket"

    name = fields.Char(
        copy=False,
        readonly=False,
        index="trigram",
        default=lambda self: _("New ticket"),
    )
    tms_order_id = fields.Many2one("tms.order", store=True)
    sale_line_id = fields.Many2one("sale.order.line")
    sale_order_id = fields.Many2one("sale.order", related="sale_line_id.order_id")
    customer_id = fields.Many2one(
        "res.partner", related="sale_line_id.order_id.partner_id"
    )
    price = fields.Float()
    available = fields.Selection(
        [("available", "Available"), ("not_available", "Not available")],
        default="available",
        readonly=True,
    )

    def write(self, vals):
        if "sale_line_id" in vals:
            vals = dict(
                vals,
                available="not_available" if vals["sale_line_id"] else "available",
            )
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New ticket")) == _("New ticket") and vals.get(
                "tms_order_id"
            ):
                trip = self.env["tms.order"].browse(vals["tms_order_id"])
                vals["name"] = f"{trip.name}-{len(trip.seat_ticket_ids) + 1}"
        return super().create(vals_list)
