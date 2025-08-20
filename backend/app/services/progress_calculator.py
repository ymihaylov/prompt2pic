class ProgressCalculator:

    def __init__(self):
        self.stages = {
            "prompt_generation": (0, 20),  # 0-20%
            "llm_processing": (20, 30),  # 20-30%
            "image_generation": (30, 90),  # 30-90%
            "archive_creation": (90, 95),  # 90-95%
            "completion": (95, 100),  # 95-100%
        }

    def get_stage_progress(self, stage: str) -> int:
        """Get starting progress for a stage"""
        return self.stages[stage][0]

    def calculate_image_progress(self, current_image: int, total_images: int) -> int:
        start, end = self.stages["image_generation"]
        stage_range = end - start

        if total_images == 0:
            return start

        progress_per_image = stage_range / total_images
        return start + int(current_image * progress_per_image)
