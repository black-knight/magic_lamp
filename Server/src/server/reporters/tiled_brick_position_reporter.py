from reporter import Reporter


class TiledBrickPositionReporter(Reporter):
    def __init__(self, valid_locations, board_recognizer, board_descriptor, tile_brick_detector, camera):
        """
        :param valid_locations Locations to search for brick in
        :param board_recognizer Board recognizer
        :param board_descriptor Board descriptor
        :param tile_brick_detector Tile brick detector
        :param camera Camera
        """
        self.valid_locations = valid_locations
        self.board_recognizer = board_recognizer
        self.board_descriptor = board_descriptor
        self.tile_brick_detector = tile_brick_detector
        self.camera = camera

    def run(self):
        """
        Waits for brick to be positioned at any of the valid positions.
        Callback function: (tile) -> ()
        """
        while not self.stopped:
            image = self.camera.read()

            self.board_descriptor.snapshot = self.board_recognizer.find_board(image, self.board_descriptor)

            if self.board_descriptor.is_recognized():
                tile = self.tile_brick_detector.find_brick_among_tiles(self.board_descriptor, self.valid_locations)
                if tile is not None:
                    self.callback_function(tile)
                    self.stop()