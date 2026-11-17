# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class TmsDriver(models.Model):
    _inherit = "tms.driver"

    @api.model_create_multi
    def create(self, vals_list):
        drivers = super().create(vals_list)
        for driver in drivers.filtered(lambda d: not d.is_external):
            self.create_driver_employee(driver)
        return drivers

    @api.model
    def update_existing_drivers_as_employees(self):
        drivers = self.env["tms.driver"].search([("is_external", "=", False)])
        for driver in drivers:
            driver.create_driver_employee(driver)

    def open_commercial_entity(self):
        res = super().open_commercial_entity()
        return res

    def create_driver_employee(self, driver):
        employee = self.env["hr.employee"].search([("name", "=", driver.name)], limit=1)

        if not employee:
            self.env["hr.employee"].create(
                {
                    "name": driver.name,
                    "work_email": driver.email,
                    "work_phone": driver.phone,
                    "work_contact_id": driver.partner_id.id,
                }
            )
