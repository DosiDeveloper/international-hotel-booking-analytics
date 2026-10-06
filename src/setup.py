import pathlib

from dotenv import load_dotenv

load_dotenv()


class Setup:
    """
    Setup configuration for the project.
    """

    def __init__(self, data_dir: str = "data") -> None:
        self.root_data_dir = pathlib.Path(data_dir)
        self.raw_data_dir = self.root_data_dir / "raw"
        self.oltp_data_dir = self.root_data_dir / "oltp"
        self.olap_data_dir = self.root_data_dir / "olap"
        self.script_sql_dir = pathlib.Path("sql")

    def create_dirs(self):
        """
        Create the necessary directories for the project.
        """
        if not self.root_data_dir.exists():
            self.root_data_dir.mkdir()
            self.raw_data_dir.mkdir()
            self.oltp_data_dir.mkdir()
            self.olap_data_dir.mkdir()
            print("Directories created successfully")
            return True
        print("Directories already exist")
        return False

    def download_data_from_drive(self):
        """
        Download data from our datalake (Google Drive).
        """
        import os

        import gdown

        url = os.getenv("DRIVE_FOLDER")
        if not url:
            print("DRIVE_FOLDER not set")
            return
        try:
            list_files = gdown.download_folder(
                url=url, output=str(self.raw_data_dir), quiet=True, skip_download=True
            )
            for file in list_files:
                if not pathlib.Path(file.local_path).exists():
                    gdown.download(
                        id=file.id,
                        output=str(self.raw_data_dir / file.path),
                        quiet=True,
                    )
                    print(f"Downloaded: {file.local_path}")
                else:
                    print(f"File already exists: {file.local_path}")
            return
        except gdown.DownloadError as e:
            print(f"Failed to download data: {e}, url: {url}")
            return
        except gdown.DownloadCancelled as e:
            print(f"Download cancelled: {e}, url: {url}")
            return


setup = Setup()

if __name__ == "__main__":
    setup.create_dirs()
    setup.download_data_from_drive()
