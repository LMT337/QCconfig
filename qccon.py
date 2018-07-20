import os
import csv
import argparse
import subprocess

results = {}


def get_anp_id(woid):
    anp_list = subprocess.check_output(["db","wo", woid]).decode('utf-8').splitlines()
    for line in anp_list:
        if 'analysis_project_id' in line:
            anp = line.split('\t')[2].strip()
            results['Anp ID'] = anp
            break
    else:
        print('Anp ID not found')
        exit()
    return anp


def anp_status_query(anp):
    anpid = 'id={}'.format(anp)
    anp_status = subprocess.check_output(["genome", "analysis-project", "list", "-f", anpid, "--show", "status",
                                          "--noheaders"]).decode('utf-8').splitlines()
    results['Anp status'] = anp_status[0]
    return anp_status[0]


def anp_show_config(woid, anp_id):
    config_status = 'Inactive'
    results['AnP show active config'] = config_status
    print('Running genome analysis-project show-config:')
    config_list = subprocess.check_output(["genome", "analysis-project", "show-config", anp_id, "--filter",
                                           "status=active", "--style=tsv"]).decode('utf-8').splitlines()

    if config_list:
        config_status = 'Active'
        results['AnP show active config'] = config_status
        with open('{}.show-config.tsv'.format(woid), 'w') as configcsv:
            for line in config_list:
                configcsv.writelines('{}\n'.format(line))
    return config_status


def anp_disk_allocation(anp_id):

    anpid = 'id={}'.format(anp_id)
    anp_allocation_list = subprocess.check_output(["genome", "analysis-project", "list", "-f", anpid, "-sh",
                                                   "environment_config_dir"]).decode('utf-8').splitlines()

    anp_allocation_dir = '{}/genome/'.format(anp_allocation_list[2])
    anp_config_yaml = '{}/genome/config.yaml'.format(anp_allocation_list[2])

    if os.path.exists(anp_allocation_dir):
        results['Anp allocation file'] = anp_config_yaml
    else:
        anp_allocation_dir = 'Allocation directory not found'
        results['Anp allocation file'] = 'Allocation directory not found'

        anp_allocation = 'Allocation directory not found'
        results['Anp allocation'] = 'Allocation directory not found'

    if os.path.isfile(anp_config_yaml):
        with open(anp_config_yaml, 'r') as configyaml:
            for line in configyaml:
                if 'disk_group_models' in line:
                    anp_allocation = line.split(':')[1].strip()
                    results['Anp allocation'] = anp_allocation
                    break
                else:
                    anp_allocation = 'Allocation not found'
                    results['Anp allocation'] = 'Allocation not found'
    else:
        anp_allocation = 'Allocation file not found'
        results['Anp allocation'] = 'Allocation file not found'

    return anp_allocation, anp_config_yaml


def anp_disk_space():
    pass
    return


def genome_analysis_project_view(anp):
    pass
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=str, dest='woid')
    args = parser.parse_args()

    woid = args.woid
    print('---{} QC Anp Summary---\n'.format(woid))
    results['woid'] = woid

    anp_id = get_anp_id(woid)

    lims_url = 'https://imp-lims.gsc.wustl.edu/entity/setup-work-order/2856457?setup_name={}'.format(woid)
    print('lims url:\n{}\n'.format(lims_url))
    results['lims url'] = lims_url

    # anp_ticket = input('Enter anp ticket id from work order:\n')
    anp_ticket = 'PLACE HOLDER'
    anp_link = 'https://jira.ris.wustl.edu/browse/{}'.format(anp_ticket)
    results['Anp ticket link'] = anp_link

    anp_status = anp_status_query(anp_id)
    config_status = anp_show_config(woid, anp_id)
    anp_allocation, anp_allocation_dir = anp_disk_allocation(anp_id)

    print('\nWork order ID: {}\nlims url: {}\nAnp ticket: {}\nAnp ticket link: {}\nAnp ID: {}\nAnp status: {}'
          '\nAnP show active config: {}\nAnp allocation: {}\nAnp allocation file: {}'
          .format(woid, lims_url, anp_ticket, anp_link, anp_id, anp_status, config_status, anp_allocation, anp_allocation_dir))


if __name__ == '__main__':
    main()