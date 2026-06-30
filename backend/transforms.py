from torchvision import models
from torchvision import transforms

weights = models.EfficientNet_B2_Weights.DEFAULT

auto_transform = weights.transforms()