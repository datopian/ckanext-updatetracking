import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.updatetracking.commands import update_tracking

class UpdatetrackingPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)

    def get_commands(self):
        return [update_tracking]