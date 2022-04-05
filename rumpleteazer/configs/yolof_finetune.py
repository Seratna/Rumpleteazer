_base_ = '../../mmdetection/configs/yolof/yolof_r50_c5_8x8_1x_coco.py'

dataset_type = 'CocoDataset'
classes = (
    # 'Ana', 'Ashe', 'Baptiste', 'Bastion', 'Brigitte',
    # 'D.Va', 'Doomfist', 'Echo', 'Genji', 'Hanzo',
    # 'Junkrat', 'L\u00facio', 'McCree', 'Mei', 'Mercy',
    # 'Moira', 'Orisa', 'Pharah', 'Reaper', 'Reinhardt',
    # 'Roadhog', 'Sigma', 'Soldier: 76', 'Sombra', 'Symmetra',
    # 'Torbj\u00f6rn', 'Tracer', 'Widowmaker', 'Winston', 'Wrecking Ball',
    # 'Zarya', 'Zenyatta', 'Baby D.Va', 'Turret', 'Teleporter',

    'Widowmaker',
)
data = dict(
    samples_per_gpu=16,
    workers_per_gpu=16,
    train=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file='/home/antares/Documents/github/coco-annotator/exports/overwatch-20210925-pre-processed.json',
        img_prefix='/home/antares/Documents/github/coco-annotator/datasets/overwatch'
    ),
    val=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file='/home/antares/Documents/github/coco-annotator/exports/overwatch-20210925-pre-processed.json',
        img_prefix='/home/antares/Documents/github/coco-annotator/datasets/overwatch'
    ),
    test=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file='/home/antares/Documents/github/coco-annotator/exports/widowmaker_pped.json',
        img_prefix='/home/antares/Documents/github/coco-annotator/datasets/widowmaker'
    )
)

# 2. model settings

# explicitly over-write all the `num_classes` field from default 80 to 5.
model = dict(
    bbox_head=dict(
        type='YOLOFHead',
        num_classes=1,
    ),
)

runner = dict(max_epochs=1000)
log_config = dict(interval=100)
checkpoint_config = dict(interval=10,
                         max_keep_ckpts=10)

load_from = '/home/antares/Documents/code/Rumpleteazer/rumpleteazer/checkpoints/yolof_r50_c5_8x8_1x_coco_20210425_024427-8e864411.pth'
