import os, sys, logging

# Need to add this line to run from project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from valsys.utils import logger
from inttests.config import TestModelConfig


def run_spawn_model():
    logger.info(f'running: run_spawn_model')
    # Import the spawn_model function from the modeling service
    from valsys.modeling.service import spawn_model

    # Import the class for the model seed configuration data
    from valsys.seeds.model import ModelSeedConfigurationData

    # Define the model seed configuration data
    model_seed_config = ModelSeedConfigurationData(
        company_name=TestModelConfig.MODEL.get('company_name'),
        ticker=TestModelConfig.MODEL.get('ticker'),
        template_name=TestModelConfig.MODEL.get('template_name'),
        proj_period=TestModelConfig.MODEL.get('proj_period'),
        hist_period=TestModelConfig.MODEL.get('hist_period'),
        industry_group=TestModelConfig.MODEL.get('industry_group'),
        start_period=TestModelConfig.MODEL.get('start_period'),
        start_date=TestModelConfig.MODEL.get('start_date'))

    # Spawn the model and obtain the new modelID
    spawned_model_id = spawn_model(model_seed_config)
    assert isinstance(spawned_model_id, str)
    return spawned_model_id


def run_tag_model(model_uid):
    logger.info(f'running: run_tag_model')
    # Import the append_tags function from the modeling service
    from valsys.modeling.service import append_tags
    # define the models uid
    # define the tags to be appended to the model
    tags_to_append = TestModelConfig.TAGS
    # append the tags
    append_tags(model_uid, tags_to_append)
    return model_uid


def run_share_model(model_uid):
    logger.info(f'running: run_share_model')

    # Import the share_model function from the modeling service
    from valsys.modeling.service import share_model
    # Import the permissions types
    from valsys.modeling.models import Permissions

    # define the email of the user the model is to be shared with
    email_to_share_to = TestModelConfig.EMAIL
    # define the permissions for the user
    permission = Permissions.VIEW
    # share the model
    share_model(model_uid, email_to_share_to, permission=permission)
    return model_uid


def run_get_module_information(model_uid):
    logger.info(f'running: run_get_module_information')
    from valsys.modeling.service import pull_model_information, pull_case

    first_case_info = pull_model_information(model_uid).first
    case = pull_case(first_case_info.uid)
    module_info = case.module_meta
    # for the test, return the a module uid
    return model_uid, module_info[0].get('children')[0].get('uid')


def run_add_child_module(model_uid, parent_module_uid):
    logger.info(f'running: run_add_child_module')

    # Import the add_child_module function from the modeling service
    from valsys.modeling.service import add_child_module, pull_model_information

    # define the name of the new module
    new_module_name = TestModelConfig.NEW_MODULE_NAME
    # go get the case uid for the model
    case_uid = pull_model_information(model_uid).first.uid
    # use the above data to add a child module
    new_module = add_child_module(parent_module_uid, new_module_name,
                                  model_uid, case_uid)
    return model_uid, new_module.uid


def run_add_line_item(model_id, module_id):
    logger.info(f'running: run_add_line_item')

    # Import the add_line_item function from the modeling service
    from valsys.modeling.service import add_line_item, pull_model_information
    # Define the required data

    line_item_name = TestModelConfig.NEW_LINE_ITEM_NAME
    line_item_order = 10

    # Get the caseID from the modelID
    case_id = pull_model_information(model_id).first.uid
    # Add the new line item
    # returns a new line line object.
    new_line_item = add_line_item(model_id=model_id,
                                  case_id=case_id,
                                  module_id=module_id,
                                  name=line_item_name,
                                  order=line_item_order)


def main():
    logger.info('running integration tests')
    model_id = run_spawn_model()
    model_id = run_tag_model(model_id)
    model_id = run_share_model(model_id)
    model_id, module_id = run_get_module_information(model_id)
    model_id, child_module_id = run_add_child_module(model_id, module_id)
    run_add_line_item(model_id, child_module_id)
    logger.info('integration tests passed ok')


if __name__ == '__main__':
    main()