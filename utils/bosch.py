import os
import uuid
from shutil import copyfile

import yaml


def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_filename = '../dataset/raw/bosch_traffic_lights/train.yaml'
    target_path = '../dataset/train'

    with open(os.path.join(script_dir, input_filename), 'r') as stream:
        anootation_data = yaml.load(stream)

    for datum in anootation_data:

        box_labels = []

        if len(datum['boxes']) == 0:
            box_labels.append('off')
        else:
            for bbox in datum['boxes']:
                box_label = bbox['label'].lower().strip()
                if box_label in [
                    'redleft', 'redright', 'redstraight', 'redstraightleft',
                ]:
                    box_label = 'red'
                elif box_label in [
                    'greenleft', 'greenright', 'greenstraight',
                    'greenstraightright', 'greenstraightleft',
                ]:
                    box_label = 'green'

                box_labels.append(box_label)

        if len(box_labels) == 1:
            source_path = os.path.abspath(
                os.path.join(
                    script_dir,
                    os.path.dirname(input_filename),
                    datum['path'],
                )
            )
            destination_dir = os.path.abspath(
                os.path.join(
                    script_dir,
                    target_path,
                    box_labels[0],
                )
            )
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            destination_path = os.path.abspath(
                os.path.join(
                    destination_dir,
                    '{}{}'.format(
                        str(uuid.uuid4()),
                        os.path.splitext(
                            os.path.basename(datum['path'])
                        )[1]
                    ),
                )
            )

            copyfile(
                source_path,
                destination_path,
            )


if __name__ == '__main__':
    run()
