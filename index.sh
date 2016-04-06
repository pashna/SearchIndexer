#!/bin/bash

zcat "$@" | python indexing.py
