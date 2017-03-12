import exifread
import json
import os
import csv
import sys
import argparse

from dateutil import parser
from datetime import datetime


DATE_TAKEN_KEY = 'Image DateTime'
DATE_ORIGINAL = 'EXIF DateTimeOriginal'
DATE_DIGITIZED = 'EXIF DateTimeDigitized'
rootdir = 'C:\Users\jonshern\Desktop\PictureSorterData'

#constants 
years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006',
            '2006', '2007', '2008', '2009', '2010', '2011',
            '2012', '2013', '2014', '2015', '2016', '2017']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class IndexItem:
    fullpath = ''
    tags = {}
    date1 = ''
    date2 = ''
    date3 = ''
    datetaken = ''

    def __init__(self, fullpath, filename, path):
        self.fullpath = fullpath
        self.filename = filename
        self.path = path

    def process_file(self):
        file = open(self.fullpath, 'rb')
        self.tags = exifread.process_file(file, details=False)
        f.close()

    def process_exif(self):
        #Format 2006:07:13 23:50:10

        if DATE_TAKEN_KEY in self.tags:
            self.date1 = self.tags[DATE_TAKEN_KEY]
        if DATE_ORIGINAL in self.tags:
            self.date2 = self.tags[DATE_ORIGINAL]
        if DATE_DIGITIZED in self.tags:
            self.date3 = self.tags[DATE_DIGITIZED]

        if self.date1:
            self.datetaken = parser.parse(str(self.date1))
        if self.date2:
            self.datetaken = parser.parse(str(self.date2))

        #considering adding file datetime / modified time also.


def path_creator(destpath, should_create_folders):
    #get a unique list of years and months
    # yearset = set()
    # for item in items:
    #     if item.year not in yearset:
    #         yearset.add(item.year)

    if should_create_folders:
        for year in years:
            for month in months:
                filepath = destpath + os.sep + year + os.sep + month
                print 'creating folder' + filepath
                if not os.path.exists(filepath):
                    os.makedirs(filepath)

    #create unknown folder
    filepath = destpath + os.sep + 'Unknown'
    os.makedirs(filepath)



        
# parser = argparse.ArgumentParser(description='Organize Photos By Date Taken')



# def create_organized_path(basepath, index_item):
    


def process_single_item(filename):
    item = IndexItem(filename, '', '')
    item.process_file()
    item.process_exif()

def write_results_to_file(items):
    with open('fileindex.csv', 'wb') as csvfile:
        fieldnames = ['filepath',
                      'filename', DATE_TAKEN_KEY, DATE_ORIGINAL, DATE_DIGITIZED, 'Date Taken']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in items:
            writer.writerow(
                {'filepath': item.filename, 'filename':item.filename,
                 DATE_TAKEN_KEY: item.date1, DATE_ORIGINAL: item.date2,
                 DATE_DIGITIZED: item.date3, 'Date Taken': item.datetaken})


def process_images():
    items = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".jpg") or filepath.endswith(".JPG"):
                item = IndexItem(filepath, file, subdir)
                item.process_file()
                item.process_exif()
                items.append(item)

    print "Processed " + str(len(items)) + " items"


    write_results_to_file(items)


def main():


    parser = argparse.ArgumentParser(
        description='Organize Pictures')
    parser.add_argument(
        '-f', '--foldercreate', help='Create the folder structure', action='store_true')
    parser.add_argument('-d', '--destpath', help='Create the folder structure', default='nopath')

    parser.add_argument('-p', '--processimages', help='Process some images', action='store_true')
    parser.add_argument('-i', '--imagepath', help='Path of images to be process', default='nopath')
    args = vars(parser.parse_args())

    if args['foldercreate']:
        if args['destpath'] != 'nopath':
            print 'create a folder'
            path_creator(args['destpath'], True)
        else:
            print 'Path missing - User the param -d to set a path'

    if args['processimages']:
        if args['imagepath'] != 'nopath':
            print 'Process some images'
        else:
            print 'Path missing - User the param -i to set a path'



if __name__ == '__main__':
    main()



