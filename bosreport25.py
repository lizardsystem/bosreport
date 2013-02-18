"""
Create monthly structure reports based on SWDES 
Equidistant (LDB) files.
"""
import datetime
import os
import csv
from os import listdir
from os.path import isfile, join


class SwdesPart(object):
    def __init__(self, header, header_two, data):
        """
        header: "4,4,0,0,1,49,31-8-2012 12:00:0"
        header_two: "TG,GN"
        data: [1, 2, 3, ...]
        """
        self.data = {}
        self.start_date = datetime.datetime.strptime(
            header.split(',')[6],
            '%d-%m-%Y %H:%M:%S')                                
        self.location, self.parameter = header_two.split(',')
        self.step_size = datetime.timedelta(minutes=15)
        
        current_dt = self.start_date
        for item in data:
            self.data[current_dt] = float(item)
            current_dt += self.step_size
        self.end_date = current_dt

    def __str__(self):
        return '%s %s from %r' % (
            self.location, self.parameter, self.start_date)


class SwdesEquidistant(object):
    """
    A simple representation of a SWDES Equidistant file
    """

    def __init__(self):
        """
        """
        self.data = {}  # keys are locations, contents are dicts with dt/Qs
        self.start_date = None
        self.end_date = None

    def import_ldb_file(self, filename):
        """Read ldb file and put data in self.data
        """
        fo = open(filename, "r")
        lines = fo.readlines()
        single_part = []
        for line in lines:
            if line[0] == '!':
                if single_part:
                    part = SwdesPart(
                        single_part[0], 
                        single_part[1], 
                        single_part[2:])
                    if part.parameter == 'Q':
                        # simple: we only store Qs
                        if not self.data.has_key(part.location):
                            self.data[part.location] = {}
                        self.data[part.location].update(part.data)
                        if not self.start_date or part.start_date < self.start_date:
                            self.start_date = part.start_date
                        if not self.end_date or part.end_date > self.end_date:
                            self.end_date = part.end_date
                        
                # Ignore and reset
                single_part = []
            else:
                single_part.append(line.strip())

        fo.close()

    def __str__(self):
        return 'We have Q values of locations %s with dates from %r to %r' % (
            ', '.join(self.data.keys()), self.start_date, self.end_date)


class SumByDay(object):
    def __init__(self, input_data, start_date, end_date):
        """Input data: {date1: value1, date2: value2, etc}"""
        self.data = {}
        self.sum_all = 0.
        for input_date, input_value in input_data.items():
            current_date = datetime.datetime(
                input_date.year, input_date.month, input_date.day)
            if current_date >= start_date and current_date < end_date:
                if not self.data.has_key(current_date):
                    self.data[current_date] = 0.0
                self.data[current_date] += input_value
                self.sum_all += input_value

    # def as_csv(self, start_date, end_date):
    #     step = datetime.timedelta(days=1)
    #     current_dt = start_date
    #     while current_dt < end_date:
    #         current_dt += step


def next_month(dt):
    """
    Calculate first of next month
    """
    year, month = dt.year, dt.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return datetime.datetime(year, month, 1)


if __name__ == '__main__':
    # import argparse  # Available from python 2.7

    # parser = argparse.ArgumentParser(
    #     description=('Create monthly structure reports based on '
    #                  'SWDES Equidistant (LDB) files.'))
    # parser.add_argument('--input_dir', metavar='input_dir', type=str, 
    #                     help='Input directory with ldb files')
    # args = parser.parse_args()
    # if args.input_dir:
    #     input_dir = args.input_dir
    # else:
    # Default
    input_dir = 'input'
    print 'input dir: %s' % input_dir

    se = SwdesEquidistant()

    # Read all ldb files
    ldb_files = [f for f in 
                 listdir(input_dir) if 
                 isfile(join(input_dir, f)) and 
                 f.endswith('.ldb')]
    print 'files: %s' % (', '.join(ldb_files))

    for ldb_filename1 in ldb_files:
        se.import_ldb_file(join(input_dir, ldb_filename1))

    # print se

    # Generate output

    # Only the ones listed in structures are in the output
    """ GEMAAL PARKSLUIZEN					GEMAAL SCHIEGEMAAL					GEMAAL VLAARDINGERDRIESLUIZEN					GEMAAL ZAAYER					WATERINGSE SLUIS		GEMAAL WESTLAND					VD BURG		SCHEVENINGEN		TOTAAL GELOOSD			GEMAAL DOLK		WINSEMIUS		TOTAAL	VERSCHIL"""

    structures = {
        'KW01': 1,
        'KW02': 2,
        'KW03': 3,
        'KW04': 4,
        'KW05': 5,
        'KW06': 6,
        'KW07': 7,
        'KW08': 8,
        'KW09': 9,
        #'KW10': 'kw10',
        'KW11': 10,
        #'KW12': 'kw12',
        #'KW13': 'kw13',
        #'KW14': 'kw14',
        }

    if se.start_date is None or se.end_date is None:
        print 'No data found, quitting.'
        quit()

    start_dt = se.start_date
    end_dt = se.end_date
    current_dt = datetime.datetime(start_dt.year, start_dt.month, 1)

    while current_dt <= end_dt:
        #result is per month
        result = {}  # date as key, then dict with col numbers and value
        current_end_dt = next_month(current_dt)
        for structure_id, structure_colnum in structures.items():
            print 'Processing column %d with month %04d-%02d...' % (
                structure_colnum, 
                current_dt.year, current_dt.month)
            dt_counter = current_dt
            while dt_counter < current_end_dt:
                if dt_counter not in result:
                    result[dt_counter] = {0: dt_counter.strftime('%m/%d/%Y %H:%M:%S')}
                result[dt_counter][structure_colnum] = se.data[structure_id].get(dt_counter, 0.)
                dt_counter += datetime.timedelta(minutes=15)
            # kw = SumByDay(se.data[structure_id], 
            #               current_dt, current_end_dt)
            # print kw.sum_all
        result_sorted = result.items()
        result_sorted.sort(key=lambda a: a[0])
        output_filename = os.path.join(
            'output', 
            'output_%04d%02d.csv' % (current_dt.year, current_dt.month))
        # fo = open(output_filename, "w")
        # for dt, values in result_sorted:
        #     values_sorted = values.items()
        #     sorted(values)
        #     values_to_file = [v[1] for v in values_sorted]
        #     fo.write(', '.join(values_to_file))
        # fo.close()

        with open(output_filename, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            for dt, values in result_sorted:
                values_sorted = values.items()
                values_sorted.sort(key=lambda a: a[0])
                spamwriter.writerow([v[1] for v in values_sorted])

        current_dt = next_month(current_dt)

    print 'Finished. The output can be found in folder output.'
