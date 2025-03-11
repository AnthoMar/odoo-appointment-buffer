from odoo import models
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class AppointmentType(models.Model):
    _inherit = "appointment.type"

    def _slots_generate(self, first_day, last_day, timezone, reference_date=None):
        """
        Generate appointment slots while ensuring a 1h30 buffer after each appointment.
        """
        # Fetch slots from super() before filtering
        slots = super()._slots_generate(first_day, last_day, timezone, reference_date)

        # Fetch only the events occurring between first_day and last_day
        blocked_times = []
        for appointment in self.env['calendar.event'].search([
            ('start', '>=', first_day),
            ('stop', '<=', last_day)
        ]):
            start_time = appointment.start - timedelta(hours=1, minutes=30)
            end_time = appointment.stop + timedelta(hours=1, minutes=30)  # Add buffer
            blocked_times.append((start_time, end_time))

        # Remove blocked slots
        valid_slots = [
            slot for slot in slots
            if not any(start <= slot['UTC'][0] < end or start < slot['UTC'][1] <= end for start, end in blocked_times)
        ]

        return valid_slots
