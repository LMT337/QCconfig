import os
import csv
import argparse
import subprocess


def get_anp_id(woid):
    anp_list = subprocess.check_output(["db","wo", woid]).decode('utf-8').splitlines()
    for line in anp_list:
        print(line)
    return


def genome_analysis_project_view(anp):
    pass
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=str, dest='woid')
    args = parser.parse_args()

    woid = args.woid
    print(woid)

    get_anp_id(woid)


if __name__ == '__main__':
    main()