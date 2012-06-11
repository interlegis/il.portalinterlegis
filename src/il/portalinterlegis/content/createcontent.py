# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
import logging
from Products.Five.utilities.marker import mark

# codigo de
# http://keeshink.blogspot.com.br/2011/05/creating-plone-content-when-installing.html
# com alteracao para usar logger
# http://collective-docs.readthedocs.org/en/latest/testing_and_debugging/logging.html#logging-from-python-code

def createObjects(parent, children):
    """This will create new objects, or modify existing ones if id's and type
    match.

    This takes two arguments: the parent to create the content in, and the
    children to create.

    Children is a list of dictionaries defined as follows:

    new_objects = [
        {   'id': 'some-id', 
            'title': 'Some Title',
            'description': 'Some Description',
            'type': 'Folder',
            'layout': 'folder_contents',
            'workflow_transition': 'retract',
            'exclude_from_nav': True,
            'children': profile_children,
            'marker_interface': marker_interface
            },
        ]
    
    * layout:               optional, it sets a different default layout
    * workflow_transition:  optional, it tries to start that state transition
        after the object is created. (You cannot directly set the workflow to 
        any state, but you must push it through legal state transitions.)
    * exclude_from_nav:     optional, excludes item from navigation
    * children:             optional, is a list of dictionaries (like this one)
    * marker_interface:     optional, a marker interface to apply

    """
    logger = logging.getLogger("Plone")
    logger.info("Creating %s in %s" % (children, parent))

    workflowTool = getToolByName(parent, "portal_workflow")

    existing = parent.objectIds()
    for new_object in children:
        if new_object['id'] in existing:
            logger.info("%s exists, skipping" % new_object['id'])
        else:
            _createObjectByType(new_object['type'], parent, \
                id=new_object['id'], title=new_object['title'], \
                description=new_object['description'])
        logger.info("Now to modify the new_object...")
        obj = parent.get(new_object['id'], None)
        if obj is None:
            logger.info("can't get new_object %s to modify it!" % new_object['id'])
        else:
            if obj.Type() != new_object['type']:
                logger.info("types don't match!")
            else:   
                if new_object.has_key('layout'): 
                    obj.setLayout(new_object['layout'])
                if new_object.has_key('workflow_transition'): 
                    try:
                        workflowTool.doActionFor(obj, 
                            new_object['workflow_transition'])
                    except WorkflowException:
                        logger.info(
                            "WARNING: couldn't do workflow transition")
                if new_object.has_key('exclude_from_nav'):
                    obj.setExcludeFromNav(new_object['exclude_from_nav'])
                if new_object.has_key('marker_interface'): 
                    mark(obj, new_object['marker_interface'])
                obj.reindexObject()
                children = new_object.get('children',[])
                if len(children) > 0:
                    createObjects(obj, children)
