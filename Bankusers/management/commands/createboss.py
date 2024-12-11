from django.core.management.base import BaseCommand
from bank.models import Bank
from Bankusers.models import Boss

class Command(BaseCommand):
    help = 'Interactively create a Boss user with all necessary fields'

    def handle(self, *args, **kwargs):
        # Prompt for each field interactively
        username = input("Username: ")
        email = input("Email: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        code_meli = input("Code Meli: ")
        password = input("Password: ")
        bank_id = input("Bank ID: ")  # Changed to bank_id
        headquarters_location = input("Headquarters Location: ")

        try:
            # Retrieve the Bank instance
            bank = Bank.objects.get(id=bank_id)  # Use bank_id here

            # Create Boss user and assign necessary fields
            boss = Boss(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                code_meli=code_meli,
                bank=bank,  # Assign the bank instance here
                headquarters_location=headquarters_location
            )
            boss.set_password(password)  # Use set_password to hash the password
            boss.save()  # Now save the instance

            self.stdout.write(self.style.SUCCESS(f'Successfully created Boss user: {boss.username}'))

        except Bank.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: Bank with the given ID does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
