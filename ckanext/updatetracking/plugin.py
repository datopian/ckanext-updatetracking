import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.updatetracking.commands import update_tracking

class UpdatetrackingPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'updatetracking')
    
    def get_commands(self):
        return [update_tracking]