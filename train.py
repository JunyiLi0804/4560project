from __future__ import absolute_import, division, print_function
import tensorflow as tf
from models.resnet import resnet_18, resnet_34, resnet_50, resnet_101, resnet_152
import config
from prepare_data import generate_datasets
import math
import numpy as np
from tensorflow import keras


# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
# from tensorflow.keras.models import Model
# import torchvision

def get_model():
    if config.model == "resnet18":
        model = resnet_18()
    if config.model == "resnet50":
        model = resnet_50()
        # model = keras.applications.ResNet50(weights = None,
        #                   input_shape=(256, 256, 3),
        #                   include_top=False)
        # model = add_new_last_layer(model, config.NUM_CLASSES)
    if config.model == "resnet50_pre":
        model = keras.applications.ResNet50(weights='imagenet',
                                            input_shape=(256, 256, 3),
                                            include_top=False)
        model = add_new_last_layer(model, config.NUM_CLASSES)
    model.build(input_shape=(None, config.image_height, config.image_width, config.channels))
    model.summary()
    return model


if __name__ == '__main__':
    # GPU settings
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

    # get the original_dataset
    train_dataset, valid_dataset, test_dataset, train_count, valid_count, test_count = generate_datasets()

    model = get_model()
    # .load_state_dict(torch.load('./models/resnet50-19c8e357.pth'))

    # define loss and optimizer
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
    optimizer = tf.keras.optimizers.Adadelta()

    train_loss = tf.keras.metrics.Mean(name='train_loss')
    train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

    valid_loss = tf.keras.metrics.Mean(name='valid_loss')
    valid_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='valid_accuracy')


    @tf.function
    def train_step(images, labels):
        with tf.GradientTape() as tape:
            predictions = model(images, training=True)
            loss = loss_object(y_true=labels, y_pred=predictions)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(grads_and_vars=zip(gradients, model.trainable_variables))

        train_loss(loss)
        train_accuracy(labels, predictions)


    @tf.function
    def valid_step(images, labels):
        predictions = model(images, training=False)
        v_loss = loss_object(labels, predictions)

        valid_loss(v_loss)
        valid_accuracy(labels, predictions)


    # start
    train_loss1 = np.zeros(config.EPOCHS)
    train_loss1 = train_loss1.astype(float)
    train_acc1 = np.zeros(config.EPOCHS)
    train_acc1 = train_acc1.astype(float)
    Valid_Loss1 = np.zeros(config.EPOCHS)
    Valid_Loss1 = Valid_Loss1.astype(float)
    Valid_acc1 = np.zeros(config.EPOCHS)
    Valid_acc1 = Valid_acc1.astype(float)
    for epoch in range(config.EPOCHS):
        train_loss.reset_states()
        train_accuracy.reset_states()
        valid_loss.reset_states()
        valid_accuracy.reset_states()
        step = 0
        for images, labels in train_dataset:
            step += 1
            train_step(images, labels)
            print("Epoch: {}/{}, step: {}/{}, loss: {:.5f}, train accuracy: {:.5f}".format(epoch + 1,
                                                                                           config.EPOCHS,
                                                                                           step,
                                                                                           math.ceil(
                                                                                               train_count / config.BATCH_SIZE),
                                                                                           train_loss.result(),
                                                                                           train_accuracy.result()))

        for valid_images, valid_labels in valid_dataset:
            valid_step(valid_images, valid_labels)

        train_loss1[epoch] = train_loss.result()
        train_acc1[epoch] = train_accuracy.result()
        Valid_Loss1[epoch] = valid_loss.result()
        Valid_acc1[epoch] = valid_accuracy.result()

        print("Epoch: {}/{}, train loss: {:.5f}, train accuracy: {:.5f}, "
              "valid loss: {:.5f}, valid accuracy: {:.5f}".format(epoch + 1,
                                                                  config.EPOCHS,
                                                                  train_loss.result(),
                                                                  train_accuracy.result(),
                                                                  valid_loss.result(),
                                                                  valid_accuracy.result()))

        if (epoch % 5 == 0):
            tf.saved_model.save(model, "resnet18_pre_{}/50".format(epoch + 1))
    for epoch in range(config.EPOCHS):
        print("epoch " + str(epoch) + ' :' + str(train_loss1[epoch]) + ',' + str(train_acc1[epoch]) + ',' + str(
            Valid_Loss1[epoch]) + ',' + str(Valid_acc1[epoch]) + ',')

    keras.models.save_model(model, config.save_model_dir)
