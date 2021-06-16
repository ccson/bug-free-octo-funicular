import ffmpeg


class VideoTranscoder(object):

    OUTPUT_FOLDER = '/completed'

    @staticmethod
    def run(imdb_id, file_extension):
        stream = ffmpeg.input(f'{imdb_id}.{file_extension}')
        stream = ffmpeg.hflip(stream)
        stream = ffmpeg.output(stream, f'{VideoTranscoder.OUTPUT_FOLDER}/{imdb_id}.h264', **{'video_bitrate': '1000'})
        ffmpeg.run(stream)
