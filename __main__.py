from utils.io import get_settings
from ui.Main import MainUI
from db.TradeMeta import TradeMetaTable
import os

settings=get_settings()
db_path=f"{settings['data_dir']}{os.sep}{settings['db_name']}.db"
mainUI= MainUI(title=settings['PROGNAME'],db_path=db_path)
mainUI.run()

# ---- MAIN
# command=args.command[0]
# if command == 'get':
	# with TradeMetaTable(db_path) as cur:
		# cur.printAllItems()
# elif command == 'add':
	# print("502: not implemented yet, u prick.")
	# #TODO check parameters
	# # with TradeMetaTable(db_path) as cur:
		# # cur.printAllItems()
