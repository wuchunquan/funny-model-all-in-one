# ToDoList
- project to make one env to use different deeplearn models

## use gpu
```shell
# 先安装好cuda这些
# nvcc --version 看版本
# 安装torch,从https://pytorch.org/get-started/locally/这里看pip命令，我的cuda11.7用这个
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

## projects
- [x] [FastSAM](https://github.com/CASIA-IVA-Lab/FastSAM)

```shell
python .\FastSAM\Inference.py --model_path .\FastSAM\models\FastSAM-x.pt --img_path .\FastSAM\images\dogs.jpg  --matting True --text_prompt "the yellow dog" --output ./
```
- [x] [rembg](https://github.com/danielgatis/rembg)
```shell
rembg i -m isnet-general-use  .\FastSAM\images\dogs.jpg .\3.png
```
- [x] [vocal-remover](https://github.com/tsurumeso/vocal-remover)
```shell
python .\vocalRemoverInference.py --input path\to\music --gpu 0
```
- [x] [GFPGAN](https://github.com/TencentARC/GFPGAN)
```shell
cd GFPGAN
python inference_gfpgan.py -i inputs/whole_imgs -o results -v 1.3 -s 2
```
- [x] [CodeFormer](https://github.com/sczhou/CodeFormer)
```shell
cd CodeFormer
python inference_codeformer.py -w 0.7 --input_path [file or dir path]
```



