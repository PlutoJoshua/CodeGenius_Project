class InitialFreezing:
    def __init__(self, model, num_unfreeze_layers=2):
        """
        모델과 언프리징할 레이어 수를 받아 초기화합니다.
        """
        self.model = model
        self.num_unfreeze_layers = num_unfreeze_layers

        # 모델의 레이어 수를 가져옴
        self.total_layers = len(self.model.transformer.h)

        # 유효성 검증
        if num_unfreeze_layers > self.total_layers:
            raise ValueError(f"num_unfreeze_layers는 모델의 총 레이어 수({self.total_layers})를 초과할 수 없습니다.")

    def freeze_all_layers(self):
        """
        모든 레이어를 프리징합니다.
        """
        for param in self.model.parameters():
            param.requires_grad = False

    def unfreeze_top_layers(self):
        """
        상위 num_unfreeze_layers 레이어를 언프리징합니다.
        """
        for layer in self.model.transformer.h[-self.num_unfreeze_layers:]:
            for param in layer.parameters():
                param.requires_grad = True

    def apply(self):
        """
        초기 프리징 및 점진적 언프리징을 적용합니다.
        """
        self.freeze_all_layers()
        self.unfreeze_top_layers()
