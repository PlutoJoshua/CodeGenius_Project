class SelectiveFreezing:
    def __init__(self, model):
        """
        모델을 받아 초기화합니다.
        """
        self.model = model
        self.total_layers = len(self.model.transformer.h)

    def freeze_layers(self, layer_indices):
        """
        주어진 레이어 인덱스의 레이어들을 프리징합니다.
        """
        self._validate_indices(layer_indices)
        for i, layer in enumerate(self.model.transformer.h):
            if i in layer_indices:
                for param in layer.parameters():
                    param.requires_grad = False

    def unfreeze_layers(self, layer_indices):
        """
        주어진 레이어 인덱스의 레이어들을 언프리징합니다.
        """
        self._validate_indices(layer_indices)
        for i, layer in enumerate(self.model.transformer.h):
            if i in layer_indices:
                for param in layer.parameters():
                    param.requires_grad = True

    def _validate_indices(self, layer_indices):
        """
        주어진 레이어 인덱스가 유효한지 확인합니다.
        """
        for index in layer_indices:
            if index < 0 or index >= self.total_layers:
                raise ValueError(f"Layer index {index} is out of range. Valid range is 0 to {self.total_layers - 1}.")


