from ultralytics import YOLO
from utils.tools import *
import argparse
import ast
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path", type=str, default="./weights/FastSAM.pt", help="model"
    )
    parser.add_argument(
        "--img_path", type=str, default="./images/dogs.jpg", help="path to image file"
    )
    parser.add_argument("--imgsz", type=int, default=1024, help="image size")
    parser.add_argument(
        "--iou",
        type=float,
        default=0.9,
        help="iou threshold for filtering the annotations",
    )
    parser.add_argument(
        "--text_prompt", type=str, default=None, help='use text prompt eg: "a dog"'
    )
    parser.add_argument(
        "--conf", type=float, default=0.4, help="object confidence threshold"
    )
    parser.add_argument(
        "--output", type=str, default="./output/", help="image save path"
    )
    parser.add_argument(
        "--matting", type=bool, default=False, help="image matting"
    )
    parser.add_argument(
        "--randomcolor", type=bool, default=True, help="mask random color"
    )
    parser.add_argument(
        "--point_prompt", type=str, default="[[0,0]]", help="[[x1,y1],[x2,y2]]"
    )
    parser.add_argument(
        "--point_label",
        type=str,
        default="[0]",
        help="[1,0] 0:background, 1:foreground",
    )
    parser.add_argument("--box_prompt", type=str, default="[0,0,0,0]", help="[x,y,w,h]")
    parser.add_argument(
        "--better_quality",
        type=str,
        default=False,
        help="better quality using morphologyEx",
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument(
        "--device", type=str, default=device, help="cuda:[0,1,2,3,4] or cpu"
    )
    parser.add_argument(
        "--retina",
        type=bool,
        default=True,
        help="draw high-resolution segmentation masks",
    )
    parser.add_argument(
        "--withContours", type=bool, default=False, help="draw the edges of the masks"
    )
    return parser.parse_args()


def main(args):
    # load model
    model = YOLO(args.model_path)
    args.point_prompt = ast.literal_eval(args.point_prompt)
    args.box_prompt = ast.literal_eval(args.box_prompt)
    args.point_label = ast.literal_eval(args.point_label)
    results = model(
        args.img_path,
        imgsz=args.imgsz,
        device=args.device,
        retina_masks=args.retina,
        iou=args.iou,
        conf=args.conf,
        max_det=100,
    )
    if args.box_prompt[2] != 0 and args.box_prompt[3] != 0:
        annotations = prompt(results, args, box=True)
        annotations = np.array([annotations])
        fast_process(
            annotations=annotations,
            args=args,
            mask_random_color=args.randomcolor,
            bbox=convert_box_xywh_to_xyxy(args.box_prompt),
        )

    elif args.text_prompt != None:
        results = format_results(results[0], 0)
        annotations = prompt(results, args, text=True)
        if args.matting and args.output:
            image = Image.open(args.img_path).convert("RGBA")
            image = np.array(image)
            image[::, ::, 3] = image[::, ::, 3] * annotations
            save_path = os.path.join(args.output, os.path.basename(args.img_path).split('.')[0] + '.png')
            Image.fromarray(image).save(save_path)
            return
        annotations = np.array([annotations])
        fast_process(
            annotations=annotations, args=args, mask_random_color=args.randomcolor
        )

    elif args.point_prompt[0] != [0, 0]:
        results = format_results(results[0], 0)
        annotations = prompt(results, args, point=True)
        # list to numpy
        annotations = np.array([annotations])
        fast_process(
            annotations=annotations,
            args=args,
            mask_random_color=args.randomcolor,
            points=args.point_prompt,
        )

    else:
        fast_process(
            annotations=results[0].masks.data,
            args=args,
            mask_random_color=args.randomcolor,
        )


def prompt(results, args, box=None, point=None, text=None):
    ori_img = cv2.imread(args.img_path)
    ori_h = ori_img.shape[0]
    ori_w = ori_img.shape[1]
    if box:
        mask, idx = box_prompt(
            results[0].masks.data,
            convert_box_xywh_to_xyxy(args.box_prompt),
            ori_h,
            ori_w,
        )
    elif point:
        mask, idx = point_prompt(
            results, args.point_prompt, args.point_label, ori_h, ori_w
        )
    elif text:
        mask, idx = text_prompt(results, args.text_prompt, args.img_path, args.device)
    else:
        return None
    return mask


def test_FastSAM():
    args = argparse.Namespace(
        model_path=r'.\models\FastSAM-x.pt',  # 请替换为你的模型路径
        img_path=r'.\images\dogs.jpg',  # 请替换为你的图像路径
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
