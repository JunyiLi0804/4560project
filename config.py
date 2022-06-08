# some training parameters
EPOCHS = 50
BATCH_SIZE = 8
NUM_CLASSES = 12
image_height = 256
image_width = 256
channels = 3
save_model_dir = r'../saved_model/resnet18'
dataset_dir = '../Dataset'
train_dir = r'../Dataset/Training'
valid_dir = r'../Dataset/Validation'
test_dir = r'../Dataset/Test'

# choose a network
# model = "resnet18"
# model = "resnet50"
model = "resnet50_pre"
