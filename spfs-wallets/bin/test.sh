#!/bin/bash

export PYTHONPATH='.:../spfs-base:../spfs-blocks:../spfs-objects'
pytest && coverage report
