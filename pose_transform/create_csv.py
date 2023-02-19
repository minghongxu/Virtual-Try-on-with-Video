import os

img_root = []
save_dir = []
json_root = img_root.replace('train_A', 'train_alphapose')
clean_json_root = img_root.replace('train_A', 'train_video2d')


img_num = len([lists for lists in os.listdir(img_root) if os.path.isfile(os.path.join(img_root, lists))])
json_num = len([lists for lists in os.listdir(json_root) if os.path.isfile(os.path.join(json_root, lists))])
num = min(img_num, json_num)

with open (os.path.join(save_dir, 'val_list.csv'), 'a+') as f:
    f.write(',A_paths,B_paths_noise,B_paths_clean\n')
    f.write('0,\"{\'gen\':[')

    for i in range(num):
        f.write('\'')
        f.write(os.path.join(img_root, str(i+1).zfill(5)+'.png'))
        f.write('\',')
    f.write('],\'ref\':[\'')
    f.write(os.path.join(img_root, '00001.png'))
    f.write('\']}\",\"{\'gen\':[')

    for i in range(num):
        f.write('\'')
        f.write(os.path.join(json_root, str(i+1).zfill(5)+'.json'))
        f.write('\',')
    f.write('],\'ref\':[\'')
    f.write(os.path.join(json_root, '00001.json'))
    f.write('\']}\",\"{\'gen\':[')
    for i in range(num):
        f.write('\'')
        f.write(os.path.join(clean_json_root, str(i+1).zfill(5)+'.json'))
        f.write('\',')
    f.write('],\'ref\':[\'')
    f.write(os.path.join(clean_json_root, '00001.json'))
    f.write('\']}\"')