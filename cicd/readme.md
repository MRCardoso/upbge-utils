# Python scripts to run by command line

## Go to the scripts folder

```
cd cicd
```

## Upload files to bucket S3

upload a file (psd, image, video) to s3 bucket, wherever file your need versioning, but is to large to store in git

### Dependencies
- [x] install and configure the aws cli
- [x] python lib `boto3`
- [x] python lib `tqdm`


```
python cloud-files.py
```

|**Argument**|**Description**|
|---|---|
|**\* Bucket**|Your bucket name|
|**\* Basedir**|The directory to map and upload selected files|
|**\* Folder**|The folder destiny in bucket|
|**Is Public**|Default=y, Options=[y/n] - let acl public-read to uploaded file|


## Upscaling Image

Upscaling a image file

### Dependencies
- [x] Download lib [realesrgan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan), and save in cicd/realesrgan-windows
- [x] python lib ffmpeg
- [x] python lib cv2
- [x] python lib numpy
- [x] python lib PIL


```
python image-processor.py
```

|**Argument**|**Description**|
|---|---|
|**\* Basedir**|The directory to map and upscaling selected files|
|**Mode**|Default=0, Options=[0/1] - The output directory to save generated file|
|**Resolution**|Default=0, Options=[0/1/2] - The scale of the GIF file|