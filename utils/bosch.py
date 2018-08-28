import os
import uuid
import glob
from shutil import copyfile

from plumbum import local
from plumbum.cmd import sh, zip, unzip, rm
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.abspath(
    os.path.join(
        SCRIPT_DIR,
        '../dataset/raw/bosch_traffic_lights/',
    )
)
TEMP_DIR = os.path.join(DATASET_DIR, 'temp')
TARGET_DIR = os.path.abspath(
    os.path.join(
        SCRIPT_DIR,
        '../dataset/train',
    )
)


def run():
    with local.cwd(DATASET_DIR):
        sh('-c', 'cat dataset_train_rgb.zip.* > dataset_train_rgb.zip')
        zip['-FF', 'dataset_train_rgb.zip', '--out', 'dataset_train_rgb_fixed.zip']()
        unzip['dataset_train_rgb_fixed.zip', '-d', TEMP_DIR]()
        rm['dataset_train_rgb_fixed.zip']['dataset_train_rgb.zip']()

    with open(os.path.join(TEMP_DIR, 'train.yaml'), 'r') as stream:
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
                    TEMP_DIR,
                    datum['path'],
                )
            )
            destination_dir = os.path.abspath(
                os.path.join(
                    TARGET_DIR,
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
