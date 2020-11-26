import os
import json
import logging
from jsonschema import validate, Draft7Validator

logging.basicConfig(filename='validate.log', filemode='w',
                    format='%(levelname)s - %(message)s')


SCHEMAS = os.listdir('task_folder/schema')
EVENTS = os.listdir('task_folder/event')


# Get json object
def json_object(folder, file_name):
    with open(f'task_folder/{folder}/{file_name}') as open_file:
        json_instance = json.load(open_file)
    return json_instance


# Finding errors according to schema, logging, accounting of processed files
def validate_event(validator, schema_name, event, event_name, events_list):
    try:
        if event['event'] == schema_name[:-7]:
            events_list.append(event_name)
            log_message = (f'{event_name} uses {schema_name} schema '
                           f'and have such errors:\n')
            errors = validator.iter_errors(event)

            for error in errors:
                log_message += f'{error.message}\n'
            logging.warning(log_message)
    except (TypeError, KeyError) as error:
        logging.warning(f'{event_name} file has no json data.\n'
                        f'Error message: {error}\n')
    return events_list


def main():

    # List of processed files with existing schema
    events_with_schema = []
    for schema_name in SCHEMAS:
        schema = json_object('schema', schema_name)

        # Schema validation
        try:
            Draft7Validator.check_schema(schema)
            validator = Draft7Validator(schema)
        except Exception as error:
            logging.warning(f'{schema_name} is not valid schema.\n'
                            f'Error message: {error}\n')

        # Json file validation
        for event_name in EVENTS:
            event = json_object('event', event_name)
            events_with_schema = validate_event(validator, schema_name, event,
                                                event_name, events_with_schema)
    events_with_no_schema = list(set(EVENTS) - set(events_with_schema))
    logging.warning(f'These events has no schema from schema folder:\n'
                    f'{events_with_no_schema}')
    logging.warning(f"to fix 'is a required property' issue - "
                    f"add this property to json file\n"
                    f"to fix 'is not of type' issue - "
                    f"change the type of this property")


if __name__ == '__main__':
    main()






