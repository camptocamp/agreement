# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    agreement_id = fields.Many2one(
        comodel_name="agreement",
        compute="_compute_agreement_id",
        store=True,
        readonly=False,
    )

    @api.depends("sale_order_ids.agreement_id")
    def _compute_agreement_id(self):
        for ticket in self:
            agreements = ticket.mapped("sale_order_ids.agreement_id")
            if not agreements:
                ticket.agreement_id = False
            elif len(agreements) == 1:
                ticket.agreement_id = agreements.id
            else:
                ticket.agreement_id = False

    @api.constrains("sale_order_ids", "agreement_id")
    def _check_unique_agreement(self):
        for ticket in self:
            agreements = ticket.mapped("sale_order_ids.agreement_id")
            if len(agreements) > 1:
                raise ValidationError(
                    self.env._("Ticket '%s' cannot have multiple different agreements.")
                    % ticket.name
                )
