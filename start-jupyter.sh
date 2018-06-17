#!/bin/bash

#
# generate configuration and password if this is the first run
#
if [ ! -f /var/tmp/zipline_init ] ; then
    jupyter notebook --generate-config
    echo "c.NotebookApp.password = ''" >> ${CONFIG_PATH}
    touch /var/tmp/zipline_init
fi

jupyter notebook -y --no-browser --notebook-dir=${PROJECT_DIR} \
    --ip='*' --allow-root --NotebookApp.token= \
    --config=${CONFIG_PATH}