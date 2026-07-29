#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:40:25 2026

@author: daniel
"""

from openmm import Platform

print("Available platforms:")

for i in range(Platform.getNumPlatforms()):
    p = Platform.getPlatform(i)
    print(" ", p.getName())

cuda = Platform.getPlatformByName("CUDA")

print("\nCUDA Properties")

for name in cuda.getPropertyNames():
    print(name, "=", cuda.getPropertyDefaultValue(name))