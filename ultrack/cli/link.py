from pathlib import Path
from typing import Optional, Sequence

import click
from napari.viewer import ViewerModel

from ultrack import link
from ultrack.cli.utils import config_option, overwrite_option, paths_argument
from ultrack.config import MainConfig


@click.command("link")
@paths_argument()
@config_option()
@click.option(
    "--channel-axis",
    "-cha",
    required=False,
    default=None,
    type=int,
    show_default=True,
    help="Channel axis, only used when input `paths` are provided",
)
@overwrite_option()
def link_cli(
    paths: Sequence[Path],
    config: MainConfig,
    channel_axis: Optional[int],
    overwrite: bool,
) -> None:
    """Links segmentation candidates adjacent in time."""

    images = tuple()
    if len(paths) > 0:
        viewer = ViewerModel()

        kwargs = {}
        if channel_axis is not None:
            kwargs["channel_axis"] = channel_axis

        images = [layer.data for layer in viewer.open(paths, **kwargs)]

    link(
        config.linking_config,
        config.data_config,
        overwrite=overwrite,
        images=images,
    )
