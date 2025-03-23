from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_invoice_proforma_pdf_report_filename(self):
        # Supprime '_proforma' du nom de fichier
        return f"{self._get_move_display_name().replace(' ', '_').replace('/', '_')}.pdf"

    def _get_invoice_pdf_proforma(self):
        """ Génère un PDF proforma sans passer le contexte 'proforma_invoice' à QWeb. """
        self.ensure_one()
        filename = self._get_invoice_proforma_pdf_report_filename()
        content, report_type = self.env['ir.actions.report']._pre_render_qweb_pdf('account.account_invoices', self.ids, data={'proforma': False})
        content_by_id = self.env['ir.actions.report']._get_splitted_report('account.account_invoices', content, report_type)
        return {
            'filename': filename,
            'filetype': 'pdf',
            'content': content_by_id[self.id],
        }
