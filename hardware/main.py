import recorder
import uploader
import os
import splitter

def main():
    recorder.run_recorder(14)
    uploader.upload_file()


if __name__ == "__main__":
    main()