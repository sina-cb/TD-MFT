# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
	# Run the external python installer template
	op('text_template').run()
	op('timer_reader').par.initialize.pulse()
	op('timer_reader').par.start.pulse()
	return

def onCreate():
	return