import argparse
import os

import tensorflow as tf
import tensorflow.contrib.slim as slim
import tensorflow.contrib.slim.nets


parser = argparse.ArgumentParser()
parser.add_argument('--image')
parser.add_argument('--model_path', default='ckpt/model', type=str)

VGG_MEAN = [123.68, 116.78, 103.94]


def main(args):
    graph = tf.Graph()
    with graph.as_default():
        image = tf.read_file(args.image)

        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.cast(image, tf.float32)
        image = tf.image.resize_image_with_crop_or_pad(image, 224, 224)
        image = image - tf.reshape(tf.constant(VGG_MEAN), [1, 1, 3])

        images = tf.expand_dims(image, axis=0)

        vgg = tf.contrib.slim.nets.vgg
        with slim.arg_scope(vgg.vgg_arg_scope()):
            logits, _ = vgg.vgg_16(images, num_classes=8, is_training=False)

        saver = tf.train.Saver()

        prediction = tf.nn.softmax(logits)

    with tf.Session(graph=graph) as sess:
        saver.restore(sess, args.model_path)
        result = sess.run(prediction)
        print(result)

if __name__ == '__main__':
    args = parser.parse_args()

    if not args.image:
        print('--image is a required argument.')
        exit(1)

    main(args)