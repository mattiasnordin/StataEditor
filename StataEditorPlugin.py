import sublime, sublime_plugin
import os
import Pywin32.setup
import win32com.client
import win32api
import tempfile
import subprocess
import re
import urllib
from urllib import request
import time
import os

settings_file = "StataEditor.sublime-settings"

# def is_running(process):
# 	""" Check if process is running """
# 	wmi = win32com.client.GetObject('winmgmts:')
# 	for p in wmi.InstancesOf('win32_process'): 
# 		if re.search(process, p.Name):
# 			return True
# 	return False

def find_files(file_ext):
	""" Create list of all files in project folders with given file extension """
	project_folders = []
	project_data = sublime.active_window().project_data()
	for i in range(0,len(project_data['folders'])):
		project_folders.append(project_data['folders'][i]['path'])
	start_time = time.time()
	for new_path in project_folders:
		for root, dirs, files in os.walk(new_path):
			for file in files:
				if file.endswith(file_ext):
					relDir = os.path.relpath(root, new_path)
					relFile = os.path.join(relDir, file)
					sublime.file_list.append(relFile)
				diff_time = time.time() - start_time
				# With huge folders, the loop can take a long time and freeze ST.
				# This condition tries to limit this problem by
				# breaking if the loop takes more than 1 second.
				# However it can only break between folders, so one huge folder
				# could still lead to memory leaks.
				if diff_time > 1:
					return

def temp_file_exists():
	""" Check a given temp file exists """
	file_name = 'emergency_close_stata_st.dta'
	tmp_dta = os.path.join(tempfile.gettempdir(), file_name)
	for file in os.listdir(tempfile.gettempdir()):
		if file == file_name:
			return True, tmp_dta
	return False, tmp_dta

def plugin_loaded():
	global settings
	settings = sublime.load_settings(settings_file)

def StataAutomate(stata_command):
	""" Launch Stata (if needed) and send commands """
	try:
		sublime.stata.DoCommandAsync(stata_command)

	except:
		# win32api.WinExec(settings.get("stata_path"))
		sublime.stata = win32com.client.Dispatch("stata.StataOLEApp")
		sublime.stata.DoCommand("cd " + getDirectory())
		sublime.stata.DoCommandAsync(stata_command)
		if settings.get("file_completions") != False:
			sublime.file_list = []
			for file_ext in settings.get("file_completions").split(","):
				find_files("." + file_ext.strip())

def getDirectory():
	var_dict = sublime.active_window().extract_variables()
	if settings.get("default_path") == "current_path":
		try:
			set_dir = "%(file_path)s" % var_dict
			set_dir = "\"" + set_dir + "\""
		except:
			try:
				set_dir = "%(project_path)s" % var_dict
				set_dir = "\"" + set_dir + "\""
			except:
				set_dir = ""
	elif settings.get("default_path") == "project_path" or settings.get("default_path") == "":
		try:
			set_dir = "%(project_path)s" % var_dict
			set_dir = "\"" + set_dir + "\""
		except:
			set_dir = ""
	else:
		set_dir = settings.get("default_path")
		set_dir = "\"" + set_dir + "\""
	return set_dir

def SelectCode(self,selection):
	all_text = ""
	len_sels = 0
	sels = self.view.sel()
	len_sels = 0
	for sel in sels:
		len_sels = len_sels + len(sel)

	if len_sels == 0 and selection == "default":
		all_text = self.view.substr(self.view.find('(?s).*',0))

	elif len_sels != 0 and selection == "default":
		for sel in sels:
			self.view.sel().add(self.view.line(sel.begin()))
			self.view.sel().add(self.view.line(sel.end()))
		
		for sel in sels:
			all_text = all_text + self.view.substr(sel) + "\n"

	elif selection == "rest_of_file":
		first_sel = sels[0]
		self.view.sel().add(self.view.line(first_sel.begin()))
		orig_sel_region = sublime.Region(first_sel.begin(),self.view.size())
		self.view.sel().add(orig_sel_region)

		for sel in sels:
			all_text = all_text + self.view.substr(sel) + "\n"

	elif selection == "line":
		for sel in sels:
			all_text = all_text + self.view.substr(self.view.line(sel)) + "\n"

	elif selection == "selection_only":
		for sel in sels:
			all_text = all_text + self.view.substr(sel) + "\n"

	if all_text[-1] != "\n":
		all_text = all_text + "\n"

	return all_text
	
class StataExecuteCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		all_text = SelectCode(self,args["Selection"])
		dofile_path = os.path.join(tempfile.gettempdir(), 'st_stata_temp.tmp')

		if settings.get("stata_version") <= 13:
			this_file = open(dofile_path,'w',encoding=settings.get("character_encoding"))

		if settings.get("stata_version") >= 14:
			this_file = open(dofile_path,'w',encoding='utf-8')

		this_file.write(all_text)
		this_file.close()
		nr_w_close = 0

		StataAutomate(str(args["Mode"]) + ' "' + dofile_path +'"')

class StataHelpExternal(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.run_command("expand_selection", {"to": "word"})
		sel = self.view.sel()[0]
		help_word = self.view.substr(sel)
		help_command = "help " + help_word

		StataAutomate(help_command)

class StataHelpInternal(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.run_command("expand_selection", {"to": "word"})
		sel = self.view.sel()[0]
		help_word = self.view.substr(sel)
		help_word = re.sub(" ","_",help_word)

		help_adress = "http://www.stata.com/help.cgi?" + help_word
		helpfile_path = os.path.join(tempfile.gettempdir(), 'st_stata_help.txt')

		try:
			a = urllib.request.urlopen(help_adress)
			source_code = a.read().decode("utf-8")
			a.close()

			regex_pattern = re.findall("<!-- END HEAD -->\n(.*?)<!-- BEGIN FOOT -->", source_code, re.DOTALL)
			help_content = re.sub("<h2>|</h2>|<pre>|</pre>|<p>|</p>|<b>|</b>|<a .*?>|</a>|<u>|</u>|<i>|</i>","",regex_pattern[0])
			help_content = re.sub("&gt;",">",help_content)
			help_content = re.sub("&lt;",">",help_content)

			with open(helpfile_path, 'w') as f:
				f.write(help_content)

			self.window = sublime.active_window()
			self.window.open_file(helpfile_path)
		
		except:
			print("Could not retrieve help file")

class StataLocal(sublime_plugin.TextCommand):
	def run(self,edit):
		sels = self.view.sel()
		for sel in sels:
			if len(sel) == 0:
				word_sel = self.view.word(sel.a)
			else:
				word_sel = sel
			word_str = self.view.substr(word_sel)
			word_str = "`"+word_str+"'"
			self.view.replace(edit,word_sel,word_str)

class StataLoad(sublime_plugin.TextCommand):
	def run(self,edit):
		sel = self.view.substr(self.view.sel()[0])
		StataAutomate("use " + sel + ", clear")

class StataForceClose(sublime_plugin.EventListener):
	""" Force Stata to close when Sublime Text closes """
	def on_close(self,view):
		# Check if there exists an open Sublime Text window
		if len(sublime.windows()) == 0:
			# Check if an active Stata session has been launched from Sublime Text
			try:
				print(sublime.stata)
				# If there is no emergency backup, prompt message and save backup, then delete the Stata session.
				if temp_file_exists()[0] == False:
					sublime.message_dialog("Stata is about to close. Restart\nSublime Text to restore the session.")
					sublime.stata.DoCommand("save " + temp_file_exists()[1] + ", replace")
					del sublime.stata
			except:
				pass

class StataRestore(sublime_plugin.EventListener):
	def on_text_command(self, view, name, args):
		# Check if an emergency backup file exists
		if temp_file_exists()[0] == True:
			rest = sublime.ok_cancel_dialog("Stata was forced to shut down as Sublime Text closed. Would you like to restore your previous session?")
			tmp_dta = temp_file_exists()[1]
			if rest == True:
				# win32api.WinExec(settings.get("stata_path"))
				sublime.stata = win32com.client.Dispatch("stata.StataOLEApp")
				sublime.stata.DoCommand("cd " + getDirectory())
				sublime.stata.DoCommand('use ' + tmp_dta + ', clear')
				os.remove(tmp_dta)
			else:
				os.remove(tmp_dta)
