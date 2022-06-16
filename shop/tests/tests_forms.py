from django.test import TestCase
import datetime
from ..forms import DateChooseForm


class DateChooseFormTest(TestCase):

    def test_fields_labels(self):
        form = DateChooseForm()
        self.assertEqual(form.fields['start'].label, 'From')
        self.assertEqual(form.fields['finish'].label, 'To')

    def test_clean_method(self):
        form_data = {'start': datetime.date.today(), 'finish': datetime.date.today() - datetime.timedelta(days=1)}
        form = DateChooseForm(data=form_data)
        self.assertFalse(form.is_valid())
