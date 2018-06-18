# Zipline Docker Image for Alpaca API

This is the Alpaca official docker container packages [zipline](https://github.com/zipline-live/zipline). With this
container image, you can easily run your Quantopian algorithm with live trading. This is
to run your algorithm in your computer, or server by yourself, and Alpaca is also desiging
a "one-click" solution to run your algorithm without having your server.

## Prerequisite

All you need is docker installed in your system.

## Usage

There are two usages for this container.  One is a Jupyter notebook enivronment for
exploration, and the other is a CLI environment to launch yoru algorithm for real money
trading.

In either case, you should set Alpaca API Key environment variables first.

```
$ export APCA_API_KEY_ID=xxxxx
$ export APCA_API_SECRET_KEY=yyyy
```

### Jupyter notebook environment

By default, the container launches a Jupyter notebook with no password on the port 8888.
You need to forward the port so you can access the notebook from your browser.

```
$ docker run -it --rm \
    -e APCA_API_KEY_ID -e APCA_API_SECRET_KEY -p 8888:8888 \
    alpacamarkets/alpaca-zipline
```

Then, open http://localhost:8888/ . You can start accessing Alpaca API immediately
on this environment.

### CLI environment

You can start a CLI environment using the same image as below.

```
# some data directory to download the bundle data
$ DATADIR=/data
# the directory where your algorithm file is located
$ ALGODIR=/algorithm
$ docker run -it --rm -e APCA_API_KEY_ID -e APCA_API_SECRET_KEY \
    -v $DATADIR:/root/.zipline/data \
    -v $ALGODIR:/work -w /work \
    alpacamarkets/alpaca-zipline bash
```

Modify `DATADIR` and `ALGODIR` for your needs. The data directory is used to store the
bundle data and better to be mounted from the host directory.  The algorithm directory
is where our algorithm file is located.

#### Download alpaca-bundle

In order to run the live trading, you still need to have a bundle data. Since zipline's default
quantopian-quandl bundle covers very limited data (3k stocks with daily only), Alpaca offers more
realistic data bundle called alpaca-bundle (8k stocks with daily/minute last 3000 bars).  From
inside the container, simply run:

```
$ zipline ingest -b alpaca-bundle
```

It may take a couple of minutes to complete.

#### Run algorithm

Once the bundle is saved, you are ready to run your algorithm.

```
$ zipline run -f /work/myalgo.py \
    --broker=alpaca --broker-uri=dummy \
    --state-file /work/state \
    --realtime-bar-target /work/realtime-bars/ \
    --bundle alpaca-bundle --data-frequency minute
```

Note the `--broker-uri` parameter is ignored with alpaca broker, but you have to specify something.
The `--state-file` is the file location where the zipline context is serialized.


## Compatibility
Quantopian runs each algorithm in Python 2, but this container is packaged in Python 3.  You may
need to adjust some of your code for Python 3.  You will also need to insert this code at the
beginning of your algorithm file that fills Quantopian's implicit import modules.

```
from zipline.api import *
import logbook
log = logbook.Logger('algo')
```

## Support
While we have verified a few algorithms runnable with this image, we are aware of many different
use cases, and we are happy to hear your issues, and please let us know. Alpaca constantly keeps
improving the image so that it covers more use cases.
