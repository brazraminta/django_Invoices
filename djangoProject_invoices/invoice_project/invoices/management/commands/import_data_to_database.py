import pandas as pd
import os
from django.core.management.base import BaseCommand
from invoices.models import Invoice
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = 'Import invoices from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help="C:/Users/Raminta/Documents/Programavimas su python 2023-12-18/Invoice Management System/Failai iš SharePoint/Gaunamu saskaitu registras.xlsx")


    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f"Failas nerastas: {excel_file}"))
            return

        # nuskaitomas failas su pandas
        df = pd.read_excel(excel_file)

        df = df.fillna({
            'projekto_nr': '',
            'tiekejas': '',
            'saskaitos_nr': '',
            'pastabos': ''
        })

        # konvertuojamos Boolean reikšmės
        # df['apmoketa_ne'] = df['apmoketa_ne'].map({'Apmokėta': True, 'Neapmokėta': False, 'nan': False})
        df['apmoketa_ne'] = df['apmoketa_ne'].map({'Apmokėta': True, 'Neapmokėta': False}).fillna(False)
        # df['skubu'] = df['skubu'].map({'skubu': True, 'Skubu': True, 'SKUBU': True, 'nan': False})
        df['skubu'] = df['skubu'].map({'skubu': True, 'Skubu': True, 'SKUBU': True}).fillna(False)
        print(df[['apmoketa_ne', 'skubu']])

        # patikrinama, kuriuose stulpeliuose yra NaN reikšmės
        nan_columns = df.isnull().any()
        print("Stulpeliai su NaN reikšmėmis:")
        print('nan stulpeliai: ', nan_columns[nan_columns == True])

        # patikrinama, kuriose eilutėse yra NaN reikšmės
        nan_rows = df[df.isnull().any(axis=1)]
        print('nan eilutės:', nan_rows)

        for _, row in df.iterrows():
            try:
                israsymo_data = pd.to_datetime(row['israsymo_data'], errors='coerce')
                apmoketi_iki = pd.to_datetime(row['apmoketi_iki'], errors='coerce')
                apmokejimo_data = pd.to_datetime(row['apmokejimo_data'], errors='coerce')

                # creating the Invoice instance
                Invoice.objects.create(
                    projekto_nr=row['projekto_nr'],
                    tiekejas=row['tiekejas'],
                    saskaitos_nr=row['saskaitos_nr'] if pd.notna(row['saskaitos_nr']) else '',
                    israsymo_data=israsymo_data if pd.notna(israsymo_data) else None,
                    apmoketi_iki=apmoketi_iki if pd.notna(apmoketi_iki) else None,
                    apmokejimo_data=apmokejimo_data if pd.notna(apmokejimo_data) else None,
                    apmoketa_ne=row['apmoketa_ne'],
                    skubu=row['skubu'],
                    pastabos=row['pastabos'] if pd.notna(row['pastabos']) else ''
                    )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Klaida importuojant eilutę: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Sėkmingai importuoti sąskaitų duomenys'))