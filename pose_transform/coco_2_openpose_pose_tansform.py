import json
import os

def read_DataStru_json(path):
    with open(path, 'r', encoding='utf-8') as load_f:
        strF = load_f.read()
        if len(strF) > 0:
            datas = json.loads(strF)
        else:
            datas = {}
    return datas



def transform(coco, coco_pos, openpose, open_pos):
    for i in range(3):
        openpose[open_pos*3 + i] = coco[coco_pos*3 + i]
    return coco, openpose


def coco_2_openpose(coco):
    openpose = [0 for i in range(54)]
    coco, openpose = transform(coco, 0, openpose, 0)
    coco, openpose = transform(coco, 6, openpose, 2)
    coco, openpose = transform(coco, 8, openpose, 3)
    coco, openpose = transform(coco, 10, openpose, 4)
    coco, openpose = transform(coco, 5, openpose, 5)
    coco, openpose = transform(coco, 7, openpose, 6)
    coco, openpose = transform(coco, 9, openpose, 7)
    coco, openpose = transform(coco, 12, openpose, 8)
    coco, openpose = transform(coco, 14, openpose, 9)
    coco, openpose = transform(coco, 16, openpose, 10)
    coco, openpose = transform(coco, 11, openpose, 11)
    coco, openpose = transform(coco, 13, openpose, 12)
    coco, openpose = transform(coco, 15, openpose, 13)
    coco, openpose = transform(coco, 2, openpose, 14)
    coco, openpose = transform(coco, 1, openpose, 15)
    coco, openpose = transform(coco, 4, openpose, 16)
    coco, openpose = transform(coco, 3, openpose, 17)

    for i in range(3):
        openpose[1*3 + i] += coco[5*3 + i] / 2
        openpose[1*3 + i] += coco[6*3 + i] / 2
    return openpose



def save_json(path, output_dir):
    data = read_DataStru_json(path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for img in data:
        coco = img['keypoints']
        openpose = coco_2_openpose(coco)

        result = {}
        result["version"] = "Alphapose"
        result["people"] = [{"pose_keypoints_2d":openpose}]

        pic_name = str(int(img["image_id"].split(".")[0])+1).zfill(5)+'.json'
        output_name = os.path.join(output_dir, pic_name)
        with open(output_name,'w') as file_obj:
            json.dump(result, file_obj)



path = [path-of-alpha-pose-result.json]
result = save_json(path, './pose_transform/dataset/danceFashion/val_256/train_alphapose')


