# TODO (krim @ 10/7/2018): reimplement with proper enum
class AnnotationTypes(object):
    FA = "vanilla-forced-alignment"
    FFA = "filtered-forced-alignment"
    BD = "bar-detection"
    SD = "slate-detection"
    TD = "tone-detection"
    ND = "noise-detection"
    OCR = "raw-ocr-output"
    TBOX = "text-box"
    FACE = "face-box"
    # TODO linguistic annotations to leverage on the LAPPS/LIF vocab
    Sentences = "segment-sentences"
    Paragraphs = "segment-paragraphs"
    Tokens = "segment-tokens"


class MediaTypes(object):
    V = "audio-video"
    A = "audio-only"
    I = "image-only"
    T = "text"
