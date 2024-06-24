
from io import StringIO
import os, unittest
from unittest.mock import patch, MagicMock


# Import the functions from your main script
from youtube_video_converter import download_audio, convert_to_mp3

test_url = 'https://www.youtube.com/watch?v=Bf7vDBBOBUA'

class TestDownloadYouTubeToMp3(unittest.TestCase):

    @patch('youtube_video_converter.YouTube')
    @patch('youtube_video_converter.on_progress')
    def test_download_audio_success(self, mock_on_progress, mock_YouTube):
        # Setup the mock objects
        mock_stream = MagicMock()
        mock_stream.download.return_value = "test_audio.mp4"
        mock_yt = MagicMock()
        mock_yt.streams.filter.return_value.first.return_value = mock_stream
        mock_YouTube.return_value = mock_yt

        url = test_url
        output_path = "."
        result = download_audio(url, output_path)
        
        # Assertions
        mock_YouTube.assert_called_with(url, on_progress_callback=mock_on_progress)
        mock_yt.streams.filter.assert_called_with(only_audio=True)
        self.assertEqual(result, "test_audio.mp4")

    @patch('youtube_video_converter.YouTube')
    def test_download_audio_failure(self, mock_YouTube):
        mock_YouTube.side_effect = Exception("Download error")
        
        url = test_url
        output_path = "."
        result = download_audio(url, output_path)
        
        self.assertIsNone(result)

    @patch('youtube_video_converter.AudioFileClip')
    @patch('youtube_video_converter.os.remove')
    def test_convert_to_mp3_success(self, mock_remove, mock_AudioFileClip):
        audio_file = "test_audio.mp4"
        mock_audio_clip = MagicMock()
        mock_AudioFileClip.return_value.__enter__.return_value = mock_audio_clip

        convert_to_mp3(audio_file)

        mock_AudioFileClip.assert_called_with(audio_file)
        mock_audio_clip.write_audiofile.assert_called_with("test_audio.mp3")
        mock_remove.assert_called_with(audio_file)

    @patch('youtube_video_converter.AudioFileClip')
    def test_convert_to_mp3_failure(self, mock_AudioFileClip):
        mock_AudioFileClip.side_effect = Exception("Conversion error")

        audio_file = "test_audio.mp4"
        convert_to_mp3(audio_file)

        mock_AudioFileClip.assert_called_with(audio_file)

if __name__ == '__main__':
    unittest.main()
