"""Common interface for candidate avatar backends."""
from abc import ABC, abstractmethod


class AvatarBackend(ABC):
    @abstractmethod
    def fit(self, video_path: str):
        """Fit/reconstruct the avatar from a patient video."""
        raise NotImplementedError

    @abstractmethod
    def render_frame(self, frame_index: int, camera=None):
        """Render one tracked frame."""
        raise NotImplementedError
