#!/bin/bash

export PYTHONPATH='.:../spfs-base'
pytest && coverage report
