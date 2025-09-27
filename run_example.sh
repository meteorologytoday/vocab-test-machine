#!/bin/bash

python3 run_test.py                                                     \
    --google-spreadsheet 1j0RLO36LHEBwA4nZ93AuDMRUiGRN2wD1UTgK0FvesVg   \
    --google-spreadsheet-gid 1211772467                                 \
    --subset-name week                                                  \
    --subset-value 2025-09-D                                            \
    --subset-type str                                                   \
    --batches 3                                                         \
    --questions-per-batch 5
