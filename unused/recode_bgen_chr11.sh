#!/usr/bin/env bash

python generate_map_file_args.py 11

qctool_v2.2.0 -g /home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bgen/wgs-genomicc-chr11.bgen -s data/bgen_recoded/genomicc-wgs/wgs-genomicc-chr11.sample -map-id-data data/map-id-file/genomicc-wgs/chr11.mapid -og data/bgen_recoded/genomicc-wgs/wgs-genomicc-chr11.bgen 
