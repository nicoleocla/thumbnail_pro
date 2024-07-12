import os
import pandas as pd
from datasets import Dataset, DatasetDict, Features, Value, Image
from huggingface_hub import HfApi, login

#Define the path to your images
current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, '..', 'data')

token = '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'

#Define the paths to your train and test CSV files
train_csv_file = os.path.join(data_dir, "summary_train_data.csv")
test_csv_file = os.path.join(data_dir, "summary_test_data.csv")

#Function to load images
def load_image(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

#Create a Huggingface dataset from the Dataframe 
def create_dataset(csv_file, split_name):
    print(f'Creating {split_name} dataset')
    df = pd.read_csv(csv_file)
    #Filter out rows with empty captions (if any)
    #df = df.dropna(subset=['caption'])
    #Load image and update the "image" column
    df['image'] = df['videoId'].map(lambda image_name: load_image(os.path.join(data_dir, f'{image_name}.jpg')))          ########
    #Remove the 'image_name' column as its no longer needed
    df = df.drop(columns=['videoId'])
    #Reset the indx to avoid '__index_level_0' column
    df = df.reset_index(drop=True)
    #Define the features of the dataset
    print(df.columns)
    features = Features({
        'image': Image(),
        'title': Value('string'),
        'viewsSubscriberRatio': Value('float32')
    })


#Create a Dataset object from the DataFrame
    dataset = Dataset.from_pandas(df, features=features)
    return dataset

#Create train and test datasets
train_dataset = create_dataset(train_csv_file, "train")
test_dataset = create_dataset(test_csv_file, "test")

#Combine into a DatasetDict
dataset_dict = DatasetDict({
    'train': train_dataset,
    'test': test_dataset
})

api = HfApi()
login(token)

#Push to Hugginface (you need to be loggedin)
dataset_dict.push_to_hub("nicoleocla/thumbnail_pro")