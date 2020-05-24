from sys import argv
import datetime
import csv


def convert(filename):
    filename_parts = filename.split('.')
    if len(filename_parts) != 2 and filename_parts[1] != 'csv':
        print('Please provide a .csv file')
        exit(-1)
    filename_out = filename_parts[0] + '_out.csv'
    with open(filename_out, mode='w') as output_csv_file:
        csv_writer = csv.writer(output_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['Date','Payee','Memo','Outflow','Inflow']
        csv_writer.writerow(fieldnames)
        with open(filename) as input_csv_file:
            csv_reader = csv.reader(input_csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    index_date = row.index('Datum')
                    index_payee = row.index('Naam / Omschrijving')
                    index_memo = row.index('Mededelingen')
                    index_credit = row.index('Af Bij')
                    index_amount = row.index('Bedrag (EUR)')
                    print('Date index = '+str(index_date))
                    print('Payee index = '+str(index_payee))
                    print('Memo index = '+str(index_memo))
                    print('Credit index = '+str(index_credit))
                    print('Amount index = '+str(index_amount))
                    line_count += 1
                else:
                    date = datetime.datetime.strptime(row[index_date],'%Y%m%d').strftime('%m/%d/%Y')
                    payee = row[index_payee]
                    memo = row[index_memo]
                    credit = (row[index_credit] == 'Af')
                    amount = row[index_amount]
                    outflow = amount if credit else None
                    inflow = amount if not credit else None
                    csv_writer.writerow([date, payee, memo, outflow, inflow])
                    line_count += 1
            print(f'Processed {line_count} lines.')


if __name__ == '__main__':
    if len(argv) < 2:
        print('Please provide input file as argument')
        exit(-1)
    filename = argv[1]
    convert(filename)
