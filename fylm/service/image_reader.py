from fylm.model.registration import RegistrationSet
from fylm.model.rotation import RotationSet
from fylm.model.timestamp import TimestampSet
from fylm.model.image import ImageSet as FylmImageSet
from itertools import izip
import logging
from nd2reader import Nd2
from fylm.service.reader import Reader
from fylm.service.base import BaseSetService

log = logging.getLogger("fylm")


class ImageReader(object):
    """
    Gets ImageSet objects from the nd2reader library, sets metadata as appropriate, applies transformations to each image
    to correct for rotational and translational distortion, and yields the ImageSet. Seamlessly gets images from separate
    ND2 files for an unlimited number of timepoints, so the application will behave as if there was only a single acquisition.

    The registration and rotation can be optionally deactivated in case they misbehave, and the start point can also be set.

    """
    def __init__(self, experiment, register_images=True, rotate_images=True):
        self._experiment = experiment
        self._field_of_view = 1
        self._register_images = register_images
        self._rotate_images = rotate_images
        self._registration_set = RegistrationSet(experiment)
        self._rotation_set = RotationSet(experiment)
        self._timestamp_set = TimestampSet(experiment)
        reader = Reader()
        set_service = BaseSetService()
        for model_set in (self._registration_set, self._rotation_set, self._timestamp_set):
            set_service.find_current(model_set)
            for model in model_set.existing:
                reader.read(model)

    @property
    def field_of_view(self):
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(self, value):
        self._field_of_view = int(value)

    def __iter__(self):
        """
        Provides image sets for all available data in order.

        """
        for timepoint, rotation_offset in zip(self._experiment.timepoints, self._rotation_set.existing):
            filename = self._experiment.get_nd2_from_timepoint(timepoint)
            try:
                nd2 = Nd2(filename)
            except Exception as e:
                log.warn("Skipping missing ND2: %s" % filename)
                continue
            registration_data = self._registration_set.get_data(self.field_of_view)
            timestamp_data = self._timestamp_set.get_data(self.field_of_view)
            for nd2_image_set, registration_offset, timestamp in izip(nd2.image_sets(self.field_of_view - 1),
                                                                      registration_data,
                                                                      timestamp_data):
                image_set = FylmImageSet(nd2_image_set, rotation_offset.offset, registration_offset, timestamp)
                yield image_set