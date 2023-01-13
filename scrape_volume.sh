#!/bin/bash
echo "" > data.txt

curl https://www.constitutionofindia.net/constitution_assembly_debates/volume/9 | \
    grep -Eo 'constitution_assembly_debates/volume/9/[^"]*' | \
    while read -r line ; do
        echo "processing $line"
        curl https://www.constitutionofindia.net/$line | \
            htmlq '.ckeditor-content .row' -p  | \
            htmlq -r .tooltiptext -r .summary-block -r .support-text -r .social-block -r .abt-events -t | \
            sed -e 's/^ *//g' |sed -e 's/\s\s\+/ /g' | \
            sed '/^$/d' | awk -i inplace '!seen[$0]++' | \
            sed 's/^: //g' | sed 's/^://g' | \
            sed 's/^9\./\n9./g' >> data.txt
    done