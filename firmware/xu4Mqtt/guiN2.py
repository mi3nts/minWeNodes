# Import tkinter and webview libraries
from tkinter import *
import webview
  
# define an instance of tkinter
tk = Tk()
  
#  size of the window where we show our website
tk.geometry("800x450")
  
# Open website
webview.create_window('MINTS', 'http://mdash.circ.utdallas.edu:3000/d/central_node_demo/central-node-demo?orgId=1&refresh=5s')
webview.start()