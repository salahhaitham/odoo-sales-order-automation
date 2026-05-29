from odoo import api,fields,models,tools
from odoo.exceptions import ValidationError


class Inherit_SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_automate_sale_order(self):
        self.ensure_one()

        if not self.partner_id:
            raise ValidationError("No customer selected!")

        if not self.order_line:
            raise ValidationError("No products added!")

        # Check stock availability
        for line in self.order_line:
            if line.product_id.type == 'product':  # Storable product
                if line.product_id.free_qty < line.product_uom_qty:
                    raise ValidationError(
                        f"Product '{line.product_id.name}' has insufficient stock!"
                    )

        # Check journal
        journal = self.env['account.journal'].search([
            ('type', '=', 'bank'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)
        if not journal:
            raise ValidationError("No payment journal available!")
        # Step 1: Confirm Sales Order
        self.action_confirm()

        # Step 2: Validate Delivery Orders
        for picking in self.picking_ids:
            picking.action_assign()  # Reserve quantities
            for move in picking.move_ids:
                move.quantity = move.product_uom_qty  # Set done quantity
            picking.button_validate()  # Validate transfer

        # Step 3 & 4: Create Invoice and Post it
        invoices = self._create_invoices()
        invoices.action_post()

        # Step 5: Register Payment
        payment_wizard = self.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=invoices.ids,
        ).create({})
        payment_wizard.action_create_payments()