import openpyxl
from django.core.management.base import BaseCommand
from documents.models import Document

class Command(BaseCommand):
    help = 'Compiles data from Document model into an Excel sheet'

    def handle(self, *args, **kwargs):
        # Retrieve documents from the Document model
        documents = Document.objects.all()

        # Check if there are any documents
        if not documents:
            self.stdout.write(self.style.WARNING('No documents found. Exiting command.'))
            return

        # Process the retrieved data
        processed_data = [{'Student Name': doc.profile.student_name, 'Email': doc.profile.email, 'File': doc.file.url} for doc in documents]

        # Export the processed data into an Excel file
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write header row
        header_row = list(processed_data[0].keys())
        sheet.append(header_row)

        # Write data rows
        for data_row in processed_data:
            sheet.append([data_row[column] for column in header_row])

        # Save the workbook
        workbook.save('compiled_data.xlsx')

        self.stdout.write(self.style.SUCCESS('Data compiled into compiled_data.xlsx'))
