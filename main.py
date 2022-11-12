import datetime
import getopt
import os
import sys

from requests import get
from logger import logger
from db import Jobs
from uuid import uuid4

# def validate_input(rule, message):
#     if not (rule):
#         print(message)
#         sys.exit(2)

def count_busday(start_date, end_date):
    all_days = (start_date + datetime.timedelta(x + 1) for x in range((end_date - start_date).days))
    count = sum(1 for day in all_days if day.weekday() < 5)
    return count


def download_file(url, output_dir):
    job_detail = {}
    try:
        res = get(url, allow_redirects=True)
        print(url)
        file_name = res.headers["Content-Disposition"].split("=", -1)[-1]
        logger.debug('Downloaded file: %s', file_name)
        saved_path = output_dir + "/" + file_name
        with open(saved_path, 'wb') as file:
            file.write(res.content)
        logger.debug("Saved: %s", saved_path)
        job_detail = {
            'id': str(uuid4()),
            'is_success': True
        }
    except:
        job_detail = {
            'id': str(uuid4()),
            'is_success': False,
            'error_message': sys.exc_info()[0]

        }
        logger.error('Error when download file with url: %s', url)
    finally:
        Jobs.insert(job_detail)

def main(argv):
    DATE_FORMAT = '%d-%m-%Y'
    timeline = datetime.datetime.strptime('2-11-2022', DATE_FORMAT)
    file_id = 5281 # WEBPXTICK_DT-20130405.gz
    # 5277 for 30/10/2022
    # start using zip: 2756 WEBPXTICK_DT-20130408.zip

    output_dir = ''
    start_date = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime(DATE_FORMAT)
    end_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATE_FORMAT)
    try:
        opts, _ = getopt.getopt(argv, 'ho:s:e:', ['outputdir=', 'startdate=', 'enddate='])
    except getopt.GetoptError:
        print('''Arguments:
        -o: output directory
        -sd: start date for extracting data
        -ed: end date for extracting data''')
        sys.exit(2)
    
    for opt, arg in opts:  # type: ignore
        if(opt == '-h'):
            print('''Arguments:
    -o, --outputdir: output directory to depositing data
    -s, --startdate: start date for extracting data
    -e, --enddate: end date for extracting data''')
            sys.exit(2)
        if(opt in ('-o', '--outputdir')):
            output_dir = arg
        if(opt in ('-s', '--startdate')):
            start_date = arg
        if(opt in ('-e', '--enddate')):
            end_date = arg

    start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date, DATE_FORMAT)
    print('output directory:', output_dir)
    print('start date:', start_date)
    print('end date:', end_date)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_id_start = file_id + count_busday(timeline, start_date)
    file_id_end = file_id + count_busday(timeline, end_date)
    print(file_id_start, file_id_end)

    for file_id in range(file_id_start, file_id_end):
        logger.debug('Dowloading file id: %s', file_id)
        url = 'https://links.sgx.com/1.0.0/derivatives-historical/{}/WEBPXTICK_DT.zip'.format(file_id)
        download_file(url, output_dir)

    print('Completed!')



if __name__ == "__main__":
    main(sys.argv[1:])
