import cv2


class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        features = []
        hist = cv2.calcHist([image], [0, 1, 2], None, self.bins, [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        features.extend(hist)
        return features
