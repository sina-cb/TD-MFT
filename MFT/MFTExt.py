"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""
import time
from TDStoreTools import StorageManager
import TDFunctions as TDF
from pymft import KnobSettings, MidiFighterTwister, constants

class MFTExt:
	"""
	MFT Wrapper Class
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.results_table = ownerComp.op('table_mft_values')
		self.config_path = tdu.expandPath(self.ownerComp.par.Configjson)
		
		self.unprocessed_data = {}
		TDF.createProperty(self, f'HasUnprocessedData',
								value=False,
								dependable=True,
								readOnly=False)		

		self.mft = None
		self.start_mft()

	def start_mft(self):
		self.mft = MidiFighterTwister()

		if not self.mft.discover():
			raise RuntimeError("Could not discover a device")

		# Configure the device
		self.mft.set_bank(constants.SystemMessages.BANK1)
		self.mft.set_aux(False)
		self.mft.config.initialize_defaults()

		# Load configuration from JSON file
		self.mft.load_config(self.config_path)
		self.mft.configure()
		self.mft.start()

	def ReadMessages(self):
		self.mft._read_messages()
		return self.mft.read_active_changed()
	
	def __delTD__(self):
		self.mft.close()