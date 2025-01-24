import sys
import os
import ckanapi
import configparser
import time
import subprocess

# from ckan.lib.cli import CkanCommand
# from ckan.common import config as ckan_config
import click

@click.command(name='update-tracking')
@click.option('--config', default='updateconfig.cfg', help='Path to config file')
def update_tracking(config):
    ''' Updates a resource with a daily tracking report
        Usage:
          update
            - Updates the resource with the new tracking report
    '''
    click.secho("Starting the tracking update process...", fg="green")
    
    PATH = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(PATH, config)
    
    parser = configparser.RawConfigParser()
    parser.read(config_path)
    
    FILENAME = parser.get('DATASET','filename')
    DATASET = parser.get('DATASET','dataset')
    SITE = parser.get('CKAN','site')
    API = parser.get('CKAN','api')

    click.secho("Configuration loaded successfully.", fg="green")

    try:
            ckan = ckanapi.RemoteCKAN(SITE, apikey=API)
    except:
            print("Ckan instance could not be initialized")
            sys.exit()
    try:
            dataset = ckan.action.package_show(id=DATASET)
    except:
            print(("Dataset: " + DATASET + " could not be found"))
            sys.exit()
    try:
           file = open(FILENAME,'rb')
    except:
           print("File was not found, creating it...")

    try:
        subprocess.run(["ckan", "tracking", "export", FILENAME], check=True)
        click.secho(f"Tracking file '{FILENAME}' generated successfully.", fg="green")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error generating the tracking file: {e}", fg="red")
        sys.exit(1)
    
    try:
        file = open(FILENAME,'rb')
    except:
        print("File was not generated")
        sys.exit()
    for i in dataset["resources"]:
        url = i["url"]
        if not url:
            url = FILENAME.split('/')[-1]
            ckan.action.resource_update(id=i["id"],package_id=i["package_id"],url=i["url"],upload=file,name=file.name,format=i["format"])
            #Trigger the datapusher hook the dirty way
            ckan.action.resource_update(id=i["id"],package_id=i["package_id"],name=file.name,format=i["format"],url=i["url"]+"&")
            ckan.action.resource_update(id=i["id"],package_id=i["package_id"],name=file.name,format=i["format"],url=url)

    sys.exit()

