#!/bin/bash

export PYTHONPATH='.:../spfs-base:../spfs-blocks:../spfs-objects:../spfs-wallets'
pytest && coverage report
