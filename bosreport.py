"""
Create monthly structure reports based on SWDES 
Equidistant (LDB) files.
"""
import datetime
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
        self.data = {}  # keys are locations, contents are Qs
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
        return 'We have Qs of locations %s with dates from %r to %r' % (
            ', '.join(self.data.keys()), self.start_date, self.end_date)


if __name__ == '__main__':
    import argparse  # Available from python 2.7

    parser = argparse.ArgumentParser(
        description=('Create monthly structure reports based on '
                     'SWDES Equidistant (LDB) files.'))
    parser.add_argument('input_dir', metavar='input_dir', type=str, 
                        help='Input directory with ldb files')
    args = parser.parse_args()
    print 'input dir: %s' % args.input_dir

    se = SwdesEquidistant()

    # Read all ldb files
    ldb_files = [f for f in 
                 listdir(args.input_dir) if 
                 isfile(join(args.input_dir, f)) and 
                 f.endswith('.ldb')]
    print 'files: %s' % (', '.join(ldb_files))

    for ldb_filename1 in ldb_files:
        se.import_ldb_file(join(args.input_dir, ldb_filename1))

    print se
