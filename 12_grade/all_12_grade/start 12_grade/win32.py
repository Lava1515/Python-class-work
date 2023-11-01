import win32api
import win32con
import win32gui
import win32ui
import ctypes
import win32com.client

# Flags = win32con.MB_OK | win32con.MB_HELP | win32con.MB_YESNO
# win32gui.MessageBox(0, "Hello", "", win32con.MB_OK)
#
# win32api.MessageBox(0, "i have a question", "bruh", win32con.MB_OK)
# n = win32ui.MessageBox("do u think yuval is Fat?", "the question ", Flags)
#
# print(n)
# my_library = ctypes.WinDLL("user32.dll")
# if n == 6:
#     my_library.MessageBoxW(0, "congrats you are corect", "right", win32con.MB_OK)
# else:
#     my_library.MessageBoxA(0, b"WRONG! yuval is fat as fuck BOYYYY", b"wrong", win32con.MB_OK)
# my_library.MessageBoxA(0, ctypes.create_string_buffer(B"yuval gay") ,ctypes.create_string_buffer(B"Facts"), Flags)
# my_library.MessageBoxA(0, b"yuval gay", b"Facts", Flags)


import win32com.client as win32
import win32com.client

word = win32.Dispatch('Word.Application')
doc = word.Documents.Add()
word.Visible = True
selection = word.Selection
selection.TypeText("BRuh")
doc.SaveAs(r"D:\ליאב\BRUH.docx")
doc.Close()
input()
word.Quit()
