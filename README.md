# Virtual-Try-on-with-Video
Traditional virtual try on can only output one picture, in other words, we can only get the generated image with the original pose of the input image. How can we generate images with different poses?

We developed a virtual try-on system. Besides accepting one cloth image and one target person image, our system also needs a short skeleton video of posing. Then we will generate a video of the target person wearing the target cloth with the same posing. 

The link of final report (blog): https://sites.google.com/view/virtual-try-on-with-video

## Pose transform
This is the [Pose-Guided Person Image Animation](https://github.com/RenYurui/Global-Flow-Local-Attention/blob/master/PERSON_IMAGE_ANIMATION.md) task from [Global-Flow-Local-Attention](https://github.com/RenYurui/Global-Flow-Local-Attention). We use its pretrained model to generate target pose video. The videos we used can be found in `./pose_transform/dataset/video`.

If you want to generate your owm video, you should extract skeleton from your video with [alpha pose](https://github.com/MVIG-SJTU/AlphaPose) first. We provide `./pose_transform/coco_2_openpose_pose_tansform.py` to tranform the outputs of alpha pose to be openpose format since Motion Extraction Net deals with openpose format skeletons.

You need extract pictures from video and place those images in `./pose_transform/dataset/danceFashion/val_256/train_A`. This command can be useful:
``` bash
ffmpeg -i ./pose_transform/dataset/video/target_pose.mp4 -r 24 -f image2 ./pose_transform/dataset/danceFashion/val_256/train_A/target_pose/%5d.png
```
By the way, transform images into video can be implemented with 
``` bash
ffmpeg -f image2 -i ./pose_transform/dataset/danceFashion/val_256/train_A/target_pose/%5d.png -vcodec libx264 -r 24 demo_video.mp4
```

The next step is using Motion Extraction Net to preprocess dirty skeletons. Assuming that you want to smooth the skeleton sequences of the fashion data set, you can use the following code:
``` bash
python ./pose_transform/test.py \
--name=dance_keypoint_checkpoints \
--model=keypoint \
--gpu_id=0 \
--dataset_mode=keypointtest \
--dataroot=./pose_transform/dataset/danceFashion \
--sub_dataset=fashionvideo \
--results_dir=./pose_transform/dataset/danceFashion/val_256/train_video2d \
--eval_set=val
```

`./pose_transform/create_csv.py` will generate a csv file which contains all the information for pose transform model. Demo csv can be found in `./pose_transform/dataset/danceFashion`.

The last step of pose tranform is generating results. Run following codes:
``` bash
python ./pose_transform/demo.py \
--name=dance_fashion_checkpoints \
--model=dance \
--attn_layer=2,3 \
--kernel_size=2=5,3=3 \
--gpu_id=0 \
--dataset_mode=dance \
--sub_dataset=fashion \
--dataroot=./pose_transform/dataset/danceFashion \
--results_dir=./demo_results/dance_fashion \
--test_list=./pose_transform/dataset/danceFashion/val_list.csv
```
## Prepare the outcome of pose transform for virtual try on
1. Run `./virtual_try_on/image_resize.py` to resize the person images from pose transform and your own cloth images to 192*256 and obtain the `test_pairs.txt` for virtual try-on model and `val.txt` for LIP_JPPNet model.
2. Use person images as input to the [LIP_JPPNet model](https://github.com/Engineering-Course/LIP_JPPNet). Run `evaluate_parsing_JPPNet-s2.py` to get the grey scale parsing result from LIP_JPPNet and then move the results into test data folder.
3. Use person images as input to the [openpose model](https://github.com/CMU-Perceptual-Computing-Lab/openpose). Run `bin\OpenPoseDemo.exe --image_dir testImage\ --write_json jsonResult\ --model_pose COCO --display 0 --render_pose 0` to get the 2d skeleton points json documents from open pose and paste into test data folder. 
4. Run `./virtual_try_on/dataset_neck_skin_correction.py` to get neck corrected person image parsing. Then Run `./virtual_try_on/body_binary_masking.py` to get person image mask.
5. Run `./virtual_try_on/cloth_mask.py` to get cloth image binary mask.

## Virtual try on
This part base on [cp-vton-plus](https://github.com/minar09/cp-vton-plus). Compared with original model, we add a discriminator to judge whether an image is real or fake to guide Try-On Module (TOM). 

New dataset can be downloaded from https://drive.google.com/file/d/1Gfut6EYSfkjElBSpGoeWG_LiAg-XeEpE/view?usp=sharing. Please unzip this file and place them in `./virtual_try_on/data/train` folder.

Then run `./virtual_try_on/test.py` to get other training data for TOM.
```
cd ./virtual_try_on
python test.py --name GMM --stage GMM --workers 4 --datamode test --data_list test_pairs.txt --checkpoint checkpoints/dataset_new/GMM/gmm_final.pth
```
This will generate the warped clothes and masks in "warp-cloth" and "warp-mask" folders inside the "./virtual_try_on/result/GMM/train/" directory. Copy the "warp-cloth" and "warp-mask" folders into your data directory, for example inside `./virtual_try_on/data/train` folder.
And then you can train your TOM model.
``` bash
cd ./virtual_try_on
python train_gan.py --name TOM --stage TOM --workers 4 --save_count 5000 --shuffle

#or train with original model
cd ./virtual_try_on
python train.py --name TOM --stage TOM --workers 4 --save_count 5000 --shuffle
```

If you want to test the performance of model, try this code:
``` bash
cd ./virtual_try_on
python test.py --name TOM --stage TOM --workers 4 --datamode test --data_list test_pairs.txt --checkpoint checkpoints/dataset_new/TOM/tom_final.pth
```

## Related resources
- [awesome-virtual-try-on](https://github.com/minar09/awesome-virtual-try-on)
- [awesome-fashion-ai](https://github.com/ayushidalmia/awesome-fashion-ai)
- [Cool Fashion Papers](https://github.com/lzhbrian/Cool-Fashion-Papers)
- [Clothes-3D](https://github.com/lzhbrian/Clothes-3D)
- [Awesome 3D Human](https://github.com/lijiaman/awesome-3d-human)
- [Awesome 3D reconstruction list](https://github.com/openMVG/awesome_3DReconstruction_list)
- [Human Body Reconstruction](https://github.com/chenweikai/Body_Reconstruction_References)
