#!/bin/bash

declare -a files=(
    "mtedx_de.tgz|https://www.openslr.org/resources/100/mtedx_de.tgz"
    "mtedx_ar.tgz|https://www.openslr.org/resources/100/mtedx_ar.tgz"
    "mtedx_el.tgz|https://www.openslr.org/resources/100/mtedx_el.tgz"
    "mtedx_ru.tgz|https://www.openslr.org/resources/100/mtedx_ru.tgz"
    "mtedx_it.tgz|https://www.openslr.org/resources/100/mtedx_it.tgz"
    "mtedx_pt.tgz|https://www.openslr.org/resources/100/mtedx_pt.tgz"
    "mtedx_fr.tgz|https://www.openslr.org/resources/100/mtedx_fr.tgz"
    "mtedx_es.tgz|https://www.openslr.org/resources/100/mtedx_es.tgz"
)

for item in "${files[@]}" ; do
    filename="${item%%|*}"
    url="${item##*|}"
    # echo "$filename    $url"
    # check if files were downloaded
    if [ -f "$filename" ]; then
        echo "$filename exists, skipped downloading"
    fi
    # check if files were extracted
    lang=${filename:6:2}
    if [ -f "$lang-$lang" ]; then
        echo "Skipped extracting $filename"
    else
        echo "Downloading $filename"
        wget $url -O $filename
        echo "Extracting $filename"
        tar zxf $filename
    fi
done
