import wave
import os
import sys

class WavMetadataExtractor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.metadata = {}

    def extract_metadata(self):
        """Extract metadata from the provided WAV file."""
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"No such file: '{self.filepath}'")
        
        try:
            with wave.open(self.filepath, 'rb') as wav_file:
                self.metadata['num_channels'] = wav_file.getnchannels()
                self.metadata['sample_width'] = wav_file.getsampwidth()
                self.metadata['frame_rate'] = wav_file.getframerate()
                self.metadata['num_frames'] = wav_file.getnframes()
                self.metadata['comptype'] = wav_file.getcomptype()
                self.metadata['compname'] = wav_file.getcompname()
                if self.metadata['frame_rate'] > 0:
                    self.metadata['duration'] = self.metadata['num_frames'] / self.metadata['frame_rate']
                else:
                    self.metadata['duration'] = 0
        except wave.Error as e:
            raise RuntimeError(f"Wave file error: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")

    def display_metadata(self):
        """Display the extracted metadata in a user-friendly format."""
        if not self.metadata:
            print("No metadata extracted. Please run extract_metadata() first.")
            return
        
        print("WAV File Metadata:")
        for key, value in self.metadata.items():
            print(f"{key}: {value}")

# TODO: Add support for reading more metadata (like ID3 tags) if needed.
# TODO: Consider adding a command-line interface for easier use.

if __name__ == "__main__":
    # Example usage:

    if len(sys.argv) != 2:
        print("Usage: python metadata_extractor.py <path_to_wav_file>")
        sys.exit(1)

    wav_file_path = sys.argv[1]
    extractor = WavMetadataExtractor(wav_file_path)
    
    try:
        extractor.extract_metadata()
        extractor.display_metadata()
    except Exception as e:
        print(f"Error: {e}")
