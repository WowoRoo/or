"""Preprocessing parameters value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PreprocessingParameters:
    """Parameters for preprocessing."""
    noise_removal_enabled: bool = True
    noise_removal_threshold: float = 0.5
    filtering_enabled: bool = True
    filter_type: str = "median"  # "gaussian", "median", etc.
    filter_size: int = 3
    binaryzation_threshold: float = 0.5

