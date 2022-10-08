from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh, xywh2xyxy
from utils.torch_utils import select_device, TracedModel
from ast import literal_eval
from PIL import Image
import numpy as np
import torch


class YoloV7Model:

    def __init__(self, weights_path: str, device_type: str, no_trace: bool,
                 img_size: int, conf_thres: float, iou_thres: float, augment: bool, agnostic_nms: bool):
        self.model, self.device = self.load_model(
            weights=weights_path,
            device_type=device_type,
            no_trace=no_trace,
            img_size=img_size
        )
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.img_size = img_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.augment = augment
        self.agnostic_nms = agnostic_nms

    @staticmethod
    def load_model(weights: str, device_type: str, no_trace: bool, img_size: int):
        device = select_device(device_type)
        half = device.type != 'cpu'

        model = attempt_load(weights, map_location=device)

        if no_trace:
            model = TracedModel(model, device, img_size)

        if half:
            model.half()  # to FP16
        print('Model loaded.')

        return model, device

    def detect(self, img, im0, imgsz):

        # stride = int(self.model.stride.max())
        # imgsz = check_img_size(self.img_size, s=stride)

        # dataset = LoadImages(image_path, img_size=imgsz, stride=stride)

        coordinates = {key: [] for key in self.names}
        # coordinates = {}
        # idx = 0

        with torch.no_grad():
            # Run inference
            if self.device.type != 'cpu':
                self.model(torch.zeros(1, 3, imgsz, imgsz).to(self.device).type_as(next(self.model.parameters())))
            old_img_w = old_img_h = imgsz
            old_img_b = 1
            # coordinates[f'frame_{idx}'] = {key: [] for key in self.names}
            # for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.device.type != 'cpu' else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            if self.device.type != 'cpu' and (
                    old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=self.augment)[0]

            pred = self.model(img, augment=self.augment)[0]
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=None,
                                       agnostic=self.agnostic_nms)

            for i, det in enumerate(pred):
                # p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
                if len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    for *xyxy, conf, cls in reversed(det):
                        coordinates[self.names[int(cls.item())]].append([int(coord.item()) for coord in xyxy])

        return coordinates

    @classmethod
    def create_model(cls, config_object):
        weights_path = config_object['YoloV7']['weights']
        device_type = config_object['YoloV7']['device_type']
        no_trace = literal_eval(config_object['YoloV7']['no_trace'])
        img_size = literal_eval(config_object['YoloV7']['img_size'])
        conf_thres = literal_eval(config_object['YoloV7']['conf_thres'])
        iou_thres = literal_eval(config_object['YoloV7']['iou_thres'])
        augment = literal_eval(config_object['YoloV7']['augment'])
        agnostic_nms = literal_eval(config_object['YoloV7']['agnostic_nms'])

        return cls(
            weights_path=weights_path,
            device_type=device_type,
            no_trace=no_trace,
            img_size=img_size,
            conf_thres=conf_thres,
            iou_thres=iou_thres,
            augment=augment,
            agnostic_nms=agnostic_nms
        )
