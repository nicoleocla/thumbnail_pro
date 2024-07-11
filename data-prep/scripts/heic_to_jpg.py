import register_heif_opener

# Register heif opener with pillow
register_heif_opener()

def convert_and_rename_heic_to_jpg(data_folder, new_prefix='chess_pieces_'):
    #iterate over all data files in the data folder
    for filename in os.listdir(data_folder):
        #check if the file is a HEIC file
        if filename.lower().endswith('.heic'):
            #Construct the full file path
            file_path = os.path.join(data_folder, filename)
            #Open the HEIC file
            image = Image.open(file_path)
        