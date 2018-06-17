from zipline.data import bundles
from click import progressbar
from io import BytesIO
import requests
import tarfile


def download_with_progress(url, chunk_size, **progress_kwargs):
    """
    Download streaming data from a URL, printing progress information to the
    terminal.

    Parameters
    ----------
    url : str
        A URL that can be understood by ``requests.get``.
    chunk_size : int
        Number of bytes to read at a time from requests.
    **progress_kwargs
        Forwarded to click.progressbar.

    Returns
    -------
    data : BytesIO
        A BytesIO containing the downloaded data.
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()

    total_size = int(resp.headers['content-length'])
    data = BytesIO()
    with progressbar(length=total_size, **progress_kwargs) as pbar:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            data.write(chunk)
            pbar.update(len(chunk))

    data.seek(0)
    return data


def download_without_progress(url):
    """
    Download data from a URL, returning a BytesIO containing the loaded data.

    Parameters
    ----------
    url : str
        A URL that can be understood by ``requests.get``.

    Returns
    -------
    data : BytesIO
        A BytesIO containing the downloaded data.
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return BytesIO(resp.content)


ALPACA_BUNDLE_URL = (
    'https://s3.amazonaws.com/files.alpaca.markets/bundle/alpaca-bundle.tgz'
)
ONE_MEGABYTE = 1024 * 1024


@bundles.register('alpaca-bundle', create_writers=False)
def alpaca_bundle(environ,
                  asset_db_writer,
                  minute_bar_writer,
                  daily_bar_writer,
                  adjustment_writer,
                  calendar,
                  start_session,
                  end_session,
                  cache,
                  show_progress,
                  output_dir):
    if show_progress:
        data = download_with_progress(
            ALPACA_BUNDLE_URL,
            chunk_size=ONE_MEGABYTE,
            label="Downloading Bundle: alpaca-bundle",
        )
    else:
        data = download_without_progress(ALPACA_BUNDLE_URL)

    with tarfile.open('r', fileobj=data) as tar:
        if show_progress:
            print("Writing data to %s." % output_dir)
        tar.extractall(output_dir)
