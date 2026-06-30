# model.py

import torch
import torch.nn as nn
import torchvision
from classes import CLASS_NAMES

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_effnetb2():
    """
    Creates EfficientNet-B2 architecture.
    """

    OUT_FEATURES = len(CLASS_NAMES)

    weights = torchvision.models.EfficientNet_B2_Weights.DEFAULT

    model = torchvision.models.efficientnet_b2(
        weights=weights
    )

    # Freeze feature extractor
    for param in model.features.parameters():
        param.requires_grad = False

    # Replace classifier
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(
            in_features=1408,
            out_features=OUT_FEATURES
        )
    )

    model.name = "effnetb2"

    return model.to(DEVICE)


def load_model():
    """
    Loads the trained weights.
    """

    model = create_effnetb2()

    model.load_state_dict(
        torch.load(
            "07_effnetb2_data_20_percent_10_epochs.pth",
            map_location=DEVICE
        )
    )

    model.eval()

    return model