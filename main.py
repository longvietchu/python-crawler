import datetime
import getopt
import os
import sys

from requests import get

def download_file(url, output_dir):
    res = get(url, allow_redirects=True)
    file_name = res.headers["Content-Disposition"].split("=", -1)[-1]
    print('Downloaded file:', file_name)
    saved_path = output_dir + "/" + file_name
    with open(saved_path, 'wb') as file:
        file.write(res.content)
    print("Saved:", saved_path)

def main(argv):
    # result = requests.get("https://links.sgx.com/1.0.0/derivatives-historical/5275/WEBPXTICK_DT.zip", allow_redirects=True)
    # open('WEBPXTICK_DT.zip', 'wb').write(result.content)
    output_dir = ''
    start_date = ''
    end_date = datetime.date.today()
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
            start_date = datetime.date.fromisoformat(arg)
        if(opt in ('-e', '--enddate')):
            end_date = datetime.date.fromisoformat(arg)

    print('output directory:', output_dir)
    print('start date:', start_date)
    print('end date:', end_date)

    # file_id = 2755 # WEBPXTICK_DT-20130405.gz
    # 5277 for 30/10/2022
    # start using zip: 2756 WEBPXTICK_DT-20130408.zip

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_id in range(5275, 5277):
        print('Dowloading file id:', file_id)
        url = 'https://links.sgx.com/1.0.0/derivatives-historical/{}/WEBPXTICK_DT.zip'.format(file_id)
        download_file(url, output_dir)

    print('Completed!')



if __name__ == "__main__":
    main(sys.argv[1:])
