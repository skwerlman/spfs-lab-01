#!/bin/bash

source bin/env.sh
pytest && coverage report
