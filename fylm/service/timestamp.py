from fylm.service.base import BaseSetService
import logging
import nd2reader

log = logging.getLogger("fylm")


class TimestampExtractor(BaseSetService):
    """
    Reads timestamps from ND2 files and writes them to disk.

    """
    def __init__(self, experiment):
        super(TimestampExtractor, self).__init__()
        self._experiment = experiment
        self._name = "timestamps"

    def save_action(self, timestamps_model):
        """
        Writes missing timestamp files.

        :type timestamps_model: fylm.model.Timestamps()

        """
        log.debug("Creating timestamps for Timepoint:%s, Field of View:%s" % (timestamps_model.timepoint,
                                                                              timestamps_model.field_of_view))
        nd2_filename = self._experiment.get_nd2_from_timepoint(timestamps_model.timepoint)
        nd2 = nd2reader.Nd2(nd2_filename)
        # subtract 1 from the field of view since nd2reader uses 0-based indexing, but we
        # refer to the fields of view with 1-based indexing
        for image_set in nd2.image_sets(field_of_view=timestamps_model.field_of_view - 1,
                                        channels=[""],
                                        z_levels=[0]):
            image = [i for i in image_set][0]
            timestamps_model.add(image.timestamp)