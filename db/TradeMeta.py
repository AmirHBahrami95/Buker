import sqlite3 as sq
import datetime

class TradeMetaTable(object):

	"""
	Meta Information about a Trade, as follows:
	1- where was i
	2- my mood
	3- when (DateTime)
	4- what (BTC/NOT/etc)
	5- profit/loss (boolean)
	6- capital_start (the total money I had before doing this trade)
	7- capital_end (total money after this trade)
	the list might get updated over time
	"""

	@staticmethod
	def getHeaders():
		return ['place','mood','what','trade_time','result','capital_start','capital_end','capital_currency']


	@staticmethod
	def getDefaults():
		return {
				'place':'homeoffice',
				'mood':'normal',
				'capital_currency':'USD'
		}

	@staticmethod
	def getEnums():
		return {
			'result':['-','+'],
			# 'capital_currency':['USD','IRL']
		}
	
	@staticmethod
	def getInts():
		return ['capital_start','capital_end']
	
	@staticmethod
	def getNonNull():
		return ['what']
	
	# --------------------------------------------------------------- init
	def __createTable(self):
		crs=self.__con.cursor()
		crs.execute("""
			create table if not exists tmeta(
				place varchar(16) not null default 'homeoffice',
				mood varchar(16) not null default 'normal',
				what varchar(16) not null,
				trade_time varchar(16) not null,
				result varchar(1) check( result in ('+','-') ) not null,
				capital_start integer,
				capital_end integer,
				capital_currency varchar(4) check( capital_currency in ('IRL','USD') ) not null default 'USD'
			)
		""")

	# call it when used outside of "with" clause
	def init(self):
		self.__con=sq.connect(self.path_to_db)
		self.__createTable()
	
	def __init__(self,path_to_db):
		self.path_to_db=path_to_db
		self.init()
	
	# --------------------------------------------------------------- insert
	def insert(self,values):
		""" {place,mood,what,trade_time,result,cap_st,cap_end,cap_curr} """
		
		# sanitize
		defs=TradeMetaTable.getDefaults()
		for i in defs:
			if i not in values or values[i]==None or len(values[i])==0:
				values[i]=defs[i]
		if 'trade_time' not in values or values['trade_time'] or len(values['trade_time'])==0:
			values['trade_time']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

		# converting to tuple (with correct order)
		tup=( 
			values['place'],
			values['mood'],
			values['what'],
			values['trade_time'],
			values['result'],
			values['capital_start'],
			values['capital_end'],
			values['capital_currency']
		); # generated by vim regex ;)
		
		# print(TradeMetaTable.getHeaders())
		# print(tup)
		crs=self.__con.cursor()
		crs.execute("insert into tmeta(place,mood,what,trade_time,result,capital_start,capital_end,capital_currency) values(?,?,?,?,?,?,?,?)",tup)
		self.__con.commit()
	
	# def insertTup(self,record):
		# """ ('homeoffice','normal','2025-02-11T19:48','BTC','-',20,19,'USD')"""
		# try:
			# crs=self.__con.cursor()
			# crs.execute("inert into tmeta values(?,?,?,?,?,?,?,?)",record)
			# self.__con.commit()
		# except:
			# pass
	
	# def insertN(self,records_list):
		# """ [ ('homeoffice','normal','2025-02-11T19:48','BTC','-',20,19,'USD'), ]"""
		# try:
			# crs=self.__con.cursor()
			# crs.executemany("insert into tmeta values(?,?,?,?,?,?,?,?)",records_list)
			# self.__con.commit()
		# except:
			# pass
	
	# --------------------------------------------------------------- select
	def __getBy(self,key,val):
		crs=self.__con.cursor()
		crs.execute("select * from tmeta where {}='{}'".format(key,val))
		return crs.fetchall()
	
	def getByWhat(self,val):
		return self.__getBy('what',val)
	
	def getByResult(self,val):
		return self.__getBy('result',val)
	
	def getByMood(self,val):
		return self.__getBy('mood',val)
	
	def getAll(self):
		crs=self.__con.cursor()
		crs.execute("select * from tmeta")
		return crs.fetchall()

	# --------------------------------------------------------------- closable
	def close(self):
		"""call this function when a TradeMeta object is used outside 'with' clause"""
		if self.__con is not None:
			self.__con.close()

	def __enter__(self):
		self.init()
		return self

	def __exit__(self,exc_type, exc_value, traceback):
		self.close()

	# --------------------------------------------------------------- etc
	def printAllItems(self):
		tupleList=self.getAll()
		for tup in tupleList:
			print(tup)

