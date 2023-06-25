import argparse
import torch

from FastSAM.Inference import parse_args, main


def test_FastSAM():
    args = argparse.Namespace(
        model_path=r'.\FastSAM\models\FastSAM-x.pt',  # 请替换为你的模型路径
        img_path=r'.\FastSAM\images\dogs.jpg',  # 请替换为你的图像路径
        imgsz=1024,
        iou=0.9,
        conf=0.4,
        matting=True,
        output='./output/',
        randomcolor=True,
        point_prompt="[[0,0]]",
        point_label="[1,0,1,0]",
        box_prompt='[0,0,0,0]',
        better_quality=False,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        retina=True,
        withContours=False,
        text_prompt="the black dog"  # 如果你想使用文本提示，可以在这里设置
    )

    # 调用main函数，进行推理
    main(args)


if __name__ == "__main__":
    args = parse_args()
    main(args)
