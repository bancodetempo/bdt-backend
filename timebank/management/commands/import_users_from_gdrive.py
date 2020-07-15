import re
import csv
from decimal import Decimal


from django.core.management.base import BaseCommand, CommandError

from authentication.models import CustomUser
from timebank.models import Account


def import_user_from_csv_row(row):
    print(row[0], row[1], row[9])
    google_drive_spreadsheet_id = re.sub('[^0-9]', '', row[0])
    user_full_name = row[1]

    if len(google_drive_spreadsheet_id) == 0:
        return

    if len(row[9]) == 0:
        current_balance = 0
    else:
        current_balance = Decimal(row[9])

    splitted_user_full_name = user_full_name.split(' ')
    first_name = splitted_user_full_name[0]
    last_name = ' '.join(splitted_user_full_name[1:])

    user_exists = CustomUser.objects.filter(
        google_drive_spreadsheet_id=google_drive_spreadsheet_id).exists()

    if not user_exists:
        user_object = {
            'first_name': first_name,
            'last_name': last_name,
            'google_drive_spreadsheet_id': google_drive_spreadsheet_id,
            'is_active': True,
            'is_staff': False
        }

        account, user = Account.create_user_with_account(
            user_object=user_object,
            balance=current_balance
        )

        account.refresh_from_db()
        print("CREATED ", user.first_name, user.last_name, account.balance)


class Command(BaseCommand):
    help = 'Imports users'

    def handle(self, *args, **options):
        filename = "bdt_072020.csv"
        self.stdout.write(self.style.SUCCESS(
            'Importing users from "%s"' % filename))
        with open(filename, newline='\n') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader]

            # User records start from 9th row
            for row in rows[9:]:
                import_user_from_csv_row(row)
