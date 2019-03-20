#!/bin/bash

pelican-themes -r pelican-left
pelican-themes -vi ../magda_space_themes/pelican-left/

pelican content
cd output && python -m pelican.server
