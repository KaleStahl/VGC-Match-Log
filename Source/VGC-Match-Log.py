# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:30:16 2023

@author: kales
"""
import tkinter as tk
import User_Interface

ux = tk.Tk()
app = User_Interface.UserInterface(ux)
app.uxInitialize(ux)