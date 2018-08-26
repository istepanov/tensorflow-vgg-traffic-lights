import os
import uuid
from shutil import copyfile

import csv


LABEL_MAP = {
    0: 'red',
    1: 'yellow',
    2: 'green',
}


def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_filename = '../dataset/raw/udacity/img_dataset.tsv'
    target_path = '../dataset/train'

    with open(os.path.join(script_dir, input_filename), 'r') as stream:
        tsv = csv.reader(stream, delimiter='\t')

        for datum in tsv:
            box_label = LABEL_MAP[int(datum[1])]

            source_path = os.path.abspath(
                os.path.join(
                    script_dir,
                    os.path.dirname(input_filename),
                    datum[0],
                )
            )
            destination_dir = os.path.abspath(
                os.path.join(
                    script_dir,
                    target_path,
                    box_label,
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
                            os.path.basename(datum[0])
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
