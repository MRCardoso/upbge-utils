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


## Generate GIF

Generate a GIF file from a video file origin

### Dependencies
- [x] python lib `ffmpeg`
- [x] python lib `cv2`

```
python video-processor.py
```

|**Argument**|**Description**|
|---|---|
|**\* Action**| Select=0, Options=[0/1] - The action to operate|
|**\* Basedir**|The directory to map and create GIF selected files|
|**Outputdir**|Default=Basedir - The output directory to save generated file|
|**Scale**|Default=600 - The scale of the GIF file|
|**FPS**|Default=10 - The fps of the GIF file|
|**Colors**|Default=128 - The amount of colors of the GIF file|

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


## Translate upbge CrossLanguange

Generate a translation for a upbge game project that have a `_language.py` file, that has the variables `texts`, `titles`

### Dependencies
- [x] python lib `googletrans`
- [x] Rename your `_language.py` to `CrossLanguage.py`
- [x] Create a file on directory `cicd` called `add_extra_path.txt`
- [x] Fill that file, with absolute path of your project source (wherever the ` _language.py` is)
- [x] Remember for translation works, the index 1 must be a empty string

### CrossLanguage.py File pattern
```
titles = {
    "new game" : ["ENGISH titles", ""],
}

texts = {
    "new game": ["ENGISH text", ""],
}
```


```
python translate.py
```

|**Argument**|**Description**|
|---|---|
|**Mode**|Default=1, Options=[(1/2] - what variable (`1- texts, 2 - titles`) will be mapped/translated|
|**Lang**|Default=pt, Options=[pt/es/jq] - The language to be translate, check the LANGUAGES var of Translate lib to check availability|