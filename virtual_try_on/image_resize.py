from PIL import Image
import os

path = ''#output path of pose transform
path_save = './data/test/image'


files = []
new_size = (192,256)
left = 30
right = 222
top = 0
bottom = 256
count_cloth = 0
count_image = 0
#f = open("cloth.txt","w")
f_LPP = open("val.txt","w")
f_test = open("test_pairs.txt","w")
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and 'vis' in i:
        #print(os.path.join(path,i))
        file_name,extension= os.path.splitext(i)
        file_path, extension = os.path.splitext(os.path.join(path_save,i))
        image = Image.open(os.path.join(path,i))
        im_crop = image.resize((192,256))
        im_crop.save(file_path + ".jpg" , 'JPEG', quality=100)
        count_cloth +=1
        f_LPP.write("/images/"+file_name +".jpg\n")
        f_test.write(file_name+".jpg"+' 008706_1.jpg\n') #change name to your own cloth image
