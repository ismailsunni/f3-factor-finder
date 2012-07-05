#!/F3/main.py
# This file contain form for classification
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-28

import random
from Tkinter import *
import tkMessageBox
from os import getcwd, makedirs, path
import tkFileDialog as tkFD
from core.util import *
from F3 import *
from datetime import datetime
import core.tweet_model as tm
import core.util as util
import copy

class ClassificationForm():
	'''GUI form for classification.'''

	def __init__(self, parent, title):
		'''Init function for ClassificationForm.'''

		self.parent = parent
		self.parent.title(title)
		self.parent.protocol("WM_DELETE_WINDOW", self.exit)
		self.init_components()
		self.FFF = F3()
		
	def init_components(self):
		'''Initialize components.'''

		# Main frame
		main_frame = Frame(self.parent, bd = 10)
		main_frame.pack(fill = BOTH, expand = YES)

		menu_bar = Menu(self.parent)
		
		# Pulldown file menu
		file_menu = Menu(menu_bar, tearoff=0)
		file_menu.add_command(label="Save Classifier", command=self.save_classifier)
		file_menu.add_command(label="Load Classifier", command=self.load_classifier)
		file_menu.add_separator()
		file_menu.add_command(label="Save Result", command=self.load_result)
		file_menu.add_command(label="Load Result", command=self.load_result)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=self.exit)
		menu_bar.add_cascade(label="File", menu=file_menu)
		
		# Pulldown help menu
		help_menu = Menu(menu_bar, tearoff=0)
		help_menu.add_command(label="About", command=self.show_about)
		help_menu.add_command(label="Help", command=self.show_help)
		menu_bar.add_cascade(label="Help", menu=help_menu)
		
		self.parent.config(menu=menu_bar)
		
		# Label User Input
		Label(main_frame, text = "Parameter Training").grid(row = 0, column = 0, columnspan = 2, sticky = W, padx = 5, pady = 5)

		# Label kata kunci
		Label(main_frame, text = "Kata Kunci").grid(row = 1, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry keyword training
		self.ent_keyword = Entry(main_frame)
		self.ent_keyword.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_keyword.insert(END, 'bad dum tss')

		# label fold
		Label(main_frame, text = "Fold").grid(row = 2, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry fold
		self.ent_fold = Entry(main_frame)
		self.ent_fold.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_fold.insert(END, '10')

		# label num_tweet training
		Label(main_frame, text = "Banyak Tweet").grid(row = 3, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry num_tweet
		self.ent_num_tweet = Entry(main_frame)
		self.ent_num_tweet.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_num_tweet.insert(END, '1000')

		# label random_seed
		Label(main_frame, text = "Random Seed").grid(row = 4, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry random_seed
		self.ent_random_seed = Entry(main_frame)
		self.ent_random_seed.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_random_seed.insert(END, '7')

		# label min_occur
		Label(main_frame, text = "Min Occur").grid(row = 5, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry min_occur
		self.ent_min_occur = Entry(main_frame)
		self.ent_min_occur.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_min_occur.insert(END, '1')

		# label parameter classify
		Label(main_frame, text = "Classify Parameter").grid(row = 7, column = 2, sticky = W, padx = 5, pady = 5, columnspan = 2)
		
		# Classify
		
		# Label kata kunci classify
		Label(main_frame, text = "Kata Kunci").grid(row = 8, column = 2, sticky = W, padx = 5, pady = 5)

		# Entry keyword classify
		self.ent_keyword_classify = Entry(main_frame)
		self.ent_keyword_classify.grid(row = 8, column = 3, padx = 5, pady = 5, sticky = W)
		self.ent_keyword_classify.insert(END, 'dahlan iskan')
		
		# Label banyak tweet classify
		Label(main_frame, text = "Num Tweet").grid(row = 9, column = 2, sticky = W, padx = 5, pady = 5)

		# Entry keyword classify
		self.ent_num_tweet_classify = Entry(main_frame)
		self.ent_num_tweet_classify.grid(row = 9, column = 3, padx = 5, pady = 5, sticky = W)
		self.ent_num_tweet_classify.insert(END, '100')
		
		# Label random classify
		Label(main_frame, text = "Random seed").grid(row = 10, column = 2, sticky = W, padx = 5, pady = 5)

		# Entry keyword classify
		self.ent_random_seed_classify = Entry(main_frame)
		self.ent_random_seed_classify.grid(row = 10, column = 3, padx = 5, pady = 5, sticky = W)
		self.ent_random_seed_classify.insert(END, '13')
		
		# show tweet
		self.show_tweet_val = IntVar()
		self.show_tweet_cb = Checkbutton(main_frame, text = "Show Tweet ?",  variable = self.show_tweet_val, onvalue = 1, offvalue = 0)
		self.show_tweet_cb.grid(row = 11, column = 2, padx = 5, pady = 5, sticky = W)
		
		# show graph or plot graph for break point detection
		self.show_graph_val = IntVar()
		self.show_graph_cb = Checkbutton(main_frame, text = "Show Graph ?",  variable = self.show_graph_val, onvalue = 1, offvalue = 0)
		self.show_graph_cb.grid(row = 12, column = 2, padx = 5, pady = 5, sticky = W)
		
		# Buttons
		# label action button
		# Label(main_frame, text = "Action Button").grid(row = 11, column = 2, sticky = W, padx = 5, pady = 5, columnspan = 2)
		
		# Button get accuracy cross validation
		self.btn_cross_validation = Button(main_frame, text = 'Hitung Akurasi', command = self.get_accuracy_cross_validation)
		self.btn_cross_validation.grid(row = 12, column = 4, padx = 5, pady = 5, sticky = W+E)

		# Button training
		self.btn_train_classifier = Button(main_frame, text = 'Train', command = self.train_classifier)
		self.btn_train_classifier.grid(row = 12, column = 5, padx = 5, pady = 5, sticky = W+E)

		# Button classify
		self.btn_classify = Button(main_frame, text = 'Classify', command = self.classify)
		self.btn_classify.grid(row = 13, column = 4, padx = 5, pady = 5, sticky = W+E)
		
		# Extract Topic
		self.btn_extract_topic = Button(main_frame, text = 'Extract Topic', command = self.extract_topic)
		self.btn_extract_topic.grid(row = 13, column = 5, padx = 5, pady = 5, sticky = W+E)
		
		# Label preprocess
		Label(main_frame, text = "Preprocess Options").grid(row = 0, column = 2, columnspan = 2, sticky = W, padx = 5, pady = 5)

		# Preprocess variables
		self.fold_case_val = IntVar()
		self.remove_rt_val = IntVar()
		self.remove_hashtag_val = IntVar()
		self.remove_username_val = IntVar()
		self.convert_number_val = IntVar()
		self.clean_number_val = IntVar()
		self.convert_emoticon_val = IntVar()
		self.remove_punctuation_string_val = IntVar()
		self.convert_word_val = IntVar()
		self.remove_stop_words_val = IntVar()
		self.convert_negation_val = IntVar()

		self.fold_case_cb = Checkbutton(main_frame, text = "Casefolding",  variable = self.fold_case_val, onvalue = 1, offvalue = 0)
		self.remove_rt_cb = Checkbutton(main_frame, text = "Remove RT",  variable = self.remove_rt_val, onvalue = 1, offvalue = 0)
		self.remove_hashtag_cb = Checkbutton(main_frame, text = "Remove Hashtag",  variable = self.remove_hashtag_val, onvalue = 1, offvalue = 0)
		self.remove_username_cb = Checkbutton(main_frame, text = "Remove Username",  variable = self.remove_username_val, onvalue = 1, offvalue = 0)
		self.convert_number_cb = Checkbutton(main_frame, text = "Convert Number",  variable = self.convert_number_val, onvalue = 1, offvalue = 0)
		self.clean_number_cb = Checkbutton(main_frame, text = "Clean Number",  variable = self.clean_number_val, onvalue = 1, offvalue = 0)
		self.convert_emoticon_cb = Checkbutton(main_frame, text = "Convert Emoticon",  variable = self.convert_emoticon_val, onvalue = 1, offvalue = 0)
		self.remove_punctuation_string_cb = Checkbutton(main_frame, text = "Remove Punctuation",  variable = self.remove_punctuation_string_val, onvalue = 1, offvalue = 0)
		self.convert_word_cb = Checkbutton(main_frame, text = "Convert Word",  variable = self.convert_word_val, onvalue = 1, offvalue = 0)
		self.remove_stop_words_cb = Checkbutton(main_frame, text = "Remove Stop Words",  variable = self.remove_stop_words_val, onvalue = 1, offvalue = 0)
		self.convert_negation_cb = Checkbutton(main_frame, text = "Convert Negation",  variable = self.convert_negation_val, onvalue = 1, offvalue = 0)

		self.fold_case_cb.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = W)
		self.remove_rt_cb.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = W)
		self.remove_hashtag_cb.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = W)
		self.remove_username_cb.grid(row = 4, column = 2, padx = 5, pady = 5, sticky = W)
		self.convert_number_cb.grid(row = 5, column = 2, padx = 5, pady = 5, sticky = W)
		self.clean_number_cb.grid(row = 6, column = 2, padx = 5, pady = 5, sticky = W)
		self.convert_emoticon_cb.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = W)
		self.remove_punctuation_string_cb.grid(row = 2, column = 3, padx = 5, pady = 5, sticky = W)
		self.convert_word_cb.grid(row = 3, column = 3, padx = 5, pady = 5, sticky = W)
		self.remove_stop_words_cb.grid(row = 4, column = 3, padx = 5, pady = 5, sticky = W)
		self.convert_negation_cb.grid(row = 5, column = 3, padx = 5, pady = 5, sticky = W)

		# Extract Topic label
		Label(main_frame, text = "Topic Extractor ").grid(row = 7, column = 0, columnspan = 2, sticky = W, padx = 5, pady = 5)
		
		# Date time label
		Label(main_frame, text = "Start date").grid(row = 8, column = 0, sticky = W, padx = 5, pady = 5)
		Label(main_frame, text = "Start time").grid(row = 9, column = 0, sticky = W, padx = 5, pady = 5)
		Label(main_frame, text = "End date").grid(row = 10, column = 0, sticky = W, padx = 5, pady = 5)
		Label(main_frame, text = "End time").grid(row = 11, column = 0, sticky = W, padx = 5, pady = 5)
		
		# Date time entry
		# Start Date
		self.ent_start_date = Entry(main_frame)
		self.ent_start_date.grid(row = 8, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_start_date.insert(END, '15-04-2012')
		# self.ent_start_date.insert(END, datetime.now().strftime('%d-%m-%Y'))
		
		# Start Time
		self.ent_start_time = Entry(main_frame)
		self.ent_start_time.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_start_time.insert(END, '02:00:00')
		
		# End Date
		self.ent_end_date = Entry(main_frame)
		self.ent_end_date.grid(row = 10, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_end_date.insert(END, '18-04-2012')
		# self.ent_end_date.insert(END, datetime.now().strftime('%d-%m-%Y'))
		
		# End Time
		self.ent_end_time = Entry(main_frame)
		self.ent_end_time.grid(row = 11, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_end_time.insert(END, '10:00:00')
		
		# Duration label
		Label(main_frame, text = "Duration").grid(row = 12, column = 0, sticky = W, padx = 5, pady = 5)
		
		# Duration entry
		self.ent_duration = Entry(main_frame)
		self.ent_duration.grid(row = 12, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_duration.insert(END, '4')
		
		# Disc Cumulative label
		Label(main_frame, text = "Disc Cumulative Factor").grid(row = 13, column = 0, sticky = W, padx = 5, pady = 5)
		
		# Duration entry
		self.ent_decay_factor = Entry(main_frame)
		self.ent_decay_factor.grid(row = 13, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_decay_factor.insert(END, '0.5')
		
		# Label output
		Label(main_frame, text = "Output").grid(row = 0, column = 4, sticky = W, padx = 5, pady = 5)

		# output text
		self.text_output = Text(main_frame, wrap = WORD)
		self.text_output.grid(row = 1, column = 4, padx = 5, pady = 5, rowspan = 11, columnspan = 2, sticky = W+E+N+S)

	def exit(self, event = None):
		'''Exit form application.'''

		self.parent.destroy()

	# show about and help form
	def show_about(self):
		'''Show about form.'''
		
		tkMessageBox.showinfo("About", "Prototipe Tugas Akhir @ismailsunni")
	
	def show_help(self):
		'''Show about form.'''
		
		tkMessageBox.showinfo("Help", "Need help? Mention me, @ismailsunni")	
	
	# classifier methods
	def get_accuracy_cross_validation(self):
		'''Get accuration for current classification.'''
		
		dict_param = {}
		try:
			fold = int(self.ent_fold.get())
			num_tweet = int(self.ent_num_tweet.get())
			random_seed = int(self.ent_random_seed.get())
			min_occur = int(self.ent_min_occur.get())
			keyword = self.ent_keyword.get()

			# Preprocess Parameter
			dict_param['fold_case'] = self.fold_case_val.get()
			dict_param['remove_RT'] = self.remove_rt_val.get()
			dict_param['remove_hashtag'] = self.remove_hashtag_val.get()
			dict_param['remove_username'] = self.remove_username_val.get()
			dict_param['convert_number'] = self.convert_number_val.get()
			dict_param['clean_number'] = self.clean_number_val.get()
			dict_param['convert_emoticon'] = self.convert_emoticon_val.get()
			dict_param['remove_punctuation_string'] = self.remove_punctuation_string_val.get()
			dict_param['convert_word'] = self.convert_word_val.get()
			dict_param['remove_stop_words'] = self.remove_stop_words_val.get()
			dict_param['convert_negation'] = self.convert_negation_val.get()

		except Exception, e:
			raise e
			debug(str(e))

		# get dev tweet for cross validation
		dev_tweets = tm.get_dev_data()
		
		# calculate the accuration
		accuration = self.FFF._classifier.get_accuracy_cross_validation(dev_tweets, num_tweet, fold, keyword, random_seed, min_occur, dict_param)
		
		# print to the output text
		self.text_output.delete('1.0', END)
		self.text_output.insert(END, 'Cross validation : ' + '\n\n')
		
		self.text_output.insert(END, 'Preprocess Parameter : ' + '\n\n')
		
		self.text_output.insert(END, 'Fold Case : ' + str(bool(dict_param['fold_case']))  + '\n')
		self.text_output.insert(END, 'Remove RT : ' + str(bool(dict_param['remove_RT'])) +'\n')
		self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(dict_param['remove_hashtag'])) + '\n')
		self.text_output.insert(END, 'Remove Username : ' + str(bool(dict_param['remove_username']))  + '\n')
		self.text_output.insert(END, 'Convert Number : ' + str(bool(dict_param['convert_number'])) + '\n')
		self.text_output.insert(END, 'Clean Number : ' + str(bool(dict_param['clean_number'])) + '\n')
		self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(dict_param['convert_emoticon'])) + '\n')
		self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(dict_param['remove_punctuation_string'])) + '\n')
		self.text_output.insert(END, 'Convert Word : ' + str(bool(dict_param['convert_word'])) + '\n')
		self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(dict_param['remove_stop_words'])) + '\n')
		self.text_output.insert(END, 'Convert Negation : ' + str(bool(dict_param['convert_negation'])) + '\n\n')

		self.text_output.insert(END, 'Fold : ' + str(fold) + '\n')
		self.text_output.insert(END, 'Banyak Tweet : ' + str(num_tweet) + '\n')
		self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
		self.text_output.insert(END, 'Minimal Kemunculan : ' + str(min_occur) + '\n\n')
		
		self.text_output.insert(END, 'Akurasi : ' + str(accuration) + '\n')

	def train_classifier(self):
		'''Train classifier.'''
		
		dict_param = {}
		try:
			fold = int(self.ent_fold.get())
			num_tweet = int(self.ent_num_tweet.get())
			random_seed = int(self.ent_random_seed.get())
			min_occur = int(self.ent_min_occur.get())
			keyword = self.ent_keyword.get()

			# parameter
			dict_param['fold_case'] = self.fold_case_val.get()
			dict_param['remove_RT'] = self.remove_rt_val.get()
			dict_param['remove_hashtag'] = self.remove_hashtag_val.get()
			dict_param['remove_username'] = self.remove_username_val.get()
			dict_param['convert_number'] = self.convert_number_val.get()
			dict_param['clean_number'] = self.clean_number_val.get()
			dict_param['convert_emoticon'] = self.convert_emoticon_val.get()
			dict_param['remove_punctuation_string'] = self.remove_punctuation_string_val.get()
			dict_param['convert_word'] = self.convert_word_val.get()
			dict_param['remove_stop_words'] = self.remove_stop_words_val.get()
			dict_param['convert_negation'] = self.convert_negation_val.get()

		except Exception, e:
			raise e
			debug(str(e))

		# get dev tweet for training
		dev_tweets = tm.get_dev_data()
		
		# train classifier
		self.FFF._classifier.train_classifier(dev_tweets, num_tweet, keyword, dict_param, min_occur)
	
		# print to the output text
		self.text_output.delete('1.0', END)
		self.text_output.insert(END, 'Training Classifier' + '\n\n')
		
		self.text_output.insert(END, 'Preprocess Parameter : ' + '\n\n')
		
		self.text_output.insert(END, 'Fold Case : ' + str(bool(dict_param['fold_case']))  + '\n')
		self.text_output.insert(END, 'Remove RT : ' + str(bool(dict_param['remove_RT'])) +'\n')
		self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(dict_param['remove_hashtag'])) + '\n')
		self.text_output.insert(END, 'Remove Username : ' + str(bool(dict_param['remove_username']))  + '\n')
		self.text_output.insert(END, 'Convert Number : ' + str(bool(dict_param['convert_number'])) + '\n')
		self.text_output.insert(END, 'Clean Number : ' + str(bool(dict_param['clean_number'])) + '\n')
		self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(dict_param['convert_emoticon'])) + '\n')
		self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(dict_param['remove_punctuation_string'])) + '\n')
		self.text_output.insert(END, 'Convert Word : ' + str(bool(dict_param['convert_word'])) + '\n')
		self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(dict_param['remove_stop_words'])) + '\n')
		self.text_output.insert(END, 'Convert Negation : ' + str(bool(dict_param['convert_negation'])) + '\n\n')

		self.text_output.insert(END, 'Banyak Tweet : ' + str(self.FFF._classifier.num_tweet_trained) + '\n')
		# self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
		self.text_output.insert(END, 'Minimal Kemunculan : ' + str(self.FFF._classifier.min_occur) + '\n\n')
		
		self.text_output.insert(END, 'Train : ' + str(self.FFF._classifier.trained) + '\n')

	def classify(self):
		'''Classify some tweets according to the current classifier.'''
		
		self.text_output.delete('1.0', END)
		
		# checking whether the classifier has been trained or not
		if not self.FFF._classifier.trained:
			self.text_output.insert(END, 'Gagal mengklasifikasikan, belum ditraining' + '\n')	
			
		else:
			try:
				num_tweet = int(self.ent_num_tweet_classify.get())
				random_seed = int(self.ent_random_seed_classify.get())
				keyword = self.ent_keyword_classify.get()
				
				# date
				start_time = datetime.strptime(self.ent_start_date.get() + ' ' + self.ent_start_time.get(), '%d-%m-%Y %H:%M:%S')
				end_time = datetime.strptime(self.ent_end_date.get() + ' ' + self.ent_end_time.get(), '%d-%m-%Y %H:%M:%S')

			except Exception, e:
				raise e
				debug(str(e))
			
			test_data = tm.get_test_data(keyword, start_time, end_time)
			if random_seed != 0:
				random.seed(random_seed)
				random.shuffle(test_data)
			list_tweet = self.FFF.classify_tweets(test_data, keyword, num_tweet)
			
			# print to the output text
			self.text_output.delete('1.0', END)
			self.text_output.insert(END, 'Hasil Klasifikasi' + '\n\n')
			self.text_output.insert(END, 'Preprocess Parameter : ' + '\n\n')
			self.text_output.insert(END, 'Fold Case : ' + str(bool(self.FFF._classifier.dict_param['fold_case']))  + '\n')
			self.text_output.insert(END, 'Remove RT : ' + str(bool(self.FFF._classifier.dict_param['remove_RT'])) +'\n')
			self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(self.FFF._classifier.dict_param['remove_hashtag'])) + '\n')
			self.text_output.insert(END, 'Remove Username : ' + str(bool(self.FFF._classifier.dict_param['remove_username']))  + '\n')
			self.text_output.insert(END, 'Convert Number : ' + str(bool(self.FFF._classifier.dict_param['convert_number'])) + '\n')
			self.text_output.insert(END, 'Clean Number : ' + str(bool(self.FFF._classifier.dict_param['clean_number'])) + '\n')
			self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(self.FFF._classifier.dict_param['convert_emoticon'])) + '\n')
			self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(self.FFF._classifier.dict_param['remove_punctuation_string'])) + '\n')
			self.text_output.insert(END, 'Convert Word : ' + str(bool(self.FFF._classifier.dict_param['convert_word'])) + '\n')
			self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(self.FFF._classifier.dict_param['remove_stop_words'])) + '\n')
			self.text_output.insert(END, 'Convert Negation : ' + str(bool(self.FFF._classifier.dict_param['convert_negation'])) + '\n\n')
			
			self.text_output.insert(END, 'Minimal Kemunculan : ' + str(self.FFF._classifier.min_occur) + '\n\n')
			
			self.text_output.insert(END, 'Keyword : ' + keyword + '\n')
			self.text_output.insert(END, 'Banyak Tweet : ' + str(self.FFF._classifier.num_tweet_classified) + '\n')
			self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
			
			
			# show result
			self.show_tweet = self.show_tweet_val.get()
			list_sentiment = []
			if self.show_tweet == 1:
				for t in list_tweet:
					self.text_output.insert(END, 'Tweet : ' + str(t.get_normal_text()) + '\n')
					self.text_output.insert(END, 'Sentiment : ' + str(t.sentiment) + '\n\n')
					list_sentiment.append(t.sentiment)
			else:
				for t in list_tweet:
					list_sentiment.append(t.sentiment)

			self.text_output.insert(END, '\n')
			self.text_output.insert(END, 'Result : \n')
			self.text_output.insert(END, 'Positif :'+ str(list_sentiment.count(1)) + ' \n')
			self.text_output.insert(END, 'Netral :'+ str(list_sentiment.count(0)) + ' \n')
			self.text_output.insert(END, 'Negatif :'+ str(list_sentiment.count(-1)) + ' \n')
			
			# this lontong function
			from xlwt import Workbook
			from tempfile import TemporaryFile
			
			book = Workbook()
			
			try:
				activeSheet = book.add_sheet(str('fuuu'))
					
				i = 1
				activeSheet.write(i, 0, 'No')
				activeSheet.write(i, 1, 'Created')
				activeSheet.write(i, 2, 'Text')
				activeSheet.write(i, 3, 'Sentiment')
				
				i += 1
				
				for tweet in list_tweet:
					activeSheet.write(i, 0, str(i - 1))
					activeSheet.write(i, 1, tweet.time.__str__())
					activeSheet.write(i, 2, str(tweet.get_normal_text()))
					activeSheet.write(i, 3, tweet.sentiment)
					
					i += 1
				pret = str(start_time).replace(':', '-')
				book.save('lontong' + pret+ '.xls')
				book.save(TemporaryFile())
			
			except Exception, e:
				util.debug(str(e))

	# extract topic method
	def extract_topic(self):
		'''Get when the breakpoints happened. Show the graph if it's selected.'''
		
		self.text_output.delete('1.0', END)
		
		# check if the data is not empty
		if self.FFF._factor_finder.list_tweet == None:
			self.text_output.insert(END, 'Failed to extract topic, list tweet is empty' + '\n')	

		else:
			# retrieve parameter			
			try:				
				# date
				start_time = datetime.strptime(self.ent_start_date.get() + ' ' + self.ent_start_time.get(), '%d-%m-%Y %H:%M:%S')
				end_time = datetime.strptime(self.ent_end_date.get() + ' ' + self.ent_end_time.get(), '%d-%m-%Y %H:%M:%S')
				duration_hour = int(self.ent_duration.get())
				decay_factor = float(self.ent_decay_factor.get())
				show_graph = bool(self.show_graph_val.get())
				
			except Exception, e:
				util.debug('retrieve parameter error')
				self.text_output.insert(END, 'Parameter error' + '\n')
			
			# to avoid long  variable name, just call it div_sent short of divide_sentiment, pffttt...
			div_sent = self.FFF._factor_finder.divide_sentiment_time(start_time, end_time, duration_hour, decay_factor)
			break_point = self.FFF._factor_finder.get_break_points()
			
			# print retval_divide_sentiment and retval_break_point to output text
			self.text_output.insert(END, 'Topic Extraction : ' + '\n\n')
			
			# topic extraction
			# topics = self.FFF._factor_finder.get_break_point_topics()
			topics_pos = self.FFF._factor_finder.get_all_topics(5, decay_factor, 1)
			topics_neg = self.FFF._factor_finder.get_all_topics(5, decay_factor, -1)
			
			self.text_output.insert(END, 'Topic Extraction parameters : ' + '\n')
			datetime.now().strftime('%d-%m-%Y')
			self.text_output.insert(END, 'Start time : ' + str(start_time) + '\n')
			self.text_output.insert(END, 'End time : ' + str(end_time) + '\n')
			self.text_output.insert(END, 'Duration : ' + str(duration_hour) + '\n')
			self.text_output.insert(END, 'Discounted Cumulative Factor : ' + str(decay_factor) + '\n\n')
		
			self.text_output.insert(END, 'No\tStart time\t\t     Num\t\tSentiment\tKumulatif\n')
			i = 0
			for idx in div_sent:
				#self.text_output.insert(END, str(i + 1) + '\t' + str(div_sent[idx]['start_time']) + '\t' + str(div_sent[idx]['end_time'])[:13] + '\t' + str(len(div_sent[idx]['list_tweet'])) + '\t\t' + str(div_sent[idx]['sentiment'])[:6] + '\t' + str(div_sent[idx]['cum_sentiment'])[:6] +'\n')
				self.text_output.insert(END, str(i + 1) + '\t' + str(div_sent[idx]['start_time']) + '\t\t' + str(len(div_sent[idx]['list_tweet'])) + '\t\t' + str(div_sent[idx]['sentiment'])[:6] + '\t' + str(div_sent[idx]['cum_sentiment'])[:6] +'\n')
				self.text_output.insert(END, '\tPositif Topics :\t'+ ',  '.join(topics_pos[idx]) + '\n')
				self.text_output.insert(END, '\tNegatif Topics :\t'+ ',  '.join(topics_neg[idx]) + '\n')
				i += 1
			
			
			# show graph or not
			if show_graph:
				self.text_output.insert(END, '\nShowing graph' + '\n')
				self.text_output.insert(END, 'Close pop up to continue' + '\n')	
				self.FFF._factor_finder.plot_graph()
	
	def extract_topic2(self):
		'''Extract topic from tweet in breakpoint duration'''
		
		print self.FFF._factor_finder.get_all_topics(5, 0.5)
		print "--------------"
		print self.FFF._factor_finder.get_all_topics(5, 0)
			
		pass
	
	# save and load classifier
	def load_classifier(self):
		'''Load classifier.'''
		
		file_opt = options = {}
		options['defaultextension'] = ''		
		options['filetypes'] = [('pickle file', '.pickle')]
		options['initialdir'] = getcwd() + '\\data'
		options['title'] = 'Load classifier'
		options['parent'] = self.parent
		
		# create dir if not exist
		if not path.exists(options['initialdir']):
			makedirs(options['initialdir'])
		
		file_name = tkFD.askopenfilename(**file_opt)
		
		if file_name:
			print file_name
			flag, self.FFF._classifier = self.FFF._classifier.load(file_name)
			self.text_output.delete('1.0', END)
			
			# print to the output text
			if flag:
				util.debug('Loaded')
				self.text_output.insert(END, 'Classifier loaded...' + '\n\n')
				
				self.text_output.insert(END, 'Preprocess Parameter : ' + '\n')
				self.text_output.insert(END, 'Fold Case : ' + str(bool(self.FFF._classifier.dict_param['fold_case']))  + '\n')
				self.text_output.insert(END, 'Remove RT : ' + str(bool(self.FFF._classifier.dict_param['remove_RT'])) +'\n')
				self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(self.FFF._classifier.dict_param['remove_hashtag'])) + '\n')
				self.text_output.insert(END, 'Remove Username : ' + str(bool(self.FFF._classifier.dict_param['remove_username']))  + '\n')
				self.text_output.insert(END, 'Convert Number : ' + str(bool(self.FFF._classifier.dict_param['convert_number'])) + '\n')
				self.text_output.insert(END, 'Clean Number : ' + str(bool(self.FFF._classifier.dict_param['clean_number'])) + '\n')
				self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(self.FFF._classifier.dict_param['convert_emoticon'])) + '\n')
				self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(self.FFF._classifier.dict_param['remove_punctuation_string'])) + '\n')
				self.text_output.insert(END, 'Convert Word : ' + str(bool(self.FFF._classifier.dict_param['convert_word'])) + '\n')
				self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(self.FFF._classifier.dict_param['remove_stop_words'])) + '\n')
				self.text_output.insert(END, 'Convert Negation : ' + str(bool(self.FFF._classifier.dict_param['convert_negation'])) + '\n\n')
				
				self.text_output.insert(END, 'Minimal Occur : ' + str(self.FFF._classifier.min_occur) + '\n')

			else:
				self.text_output.insert(END, 'Failed to load classifier...')
				util.debug('Failed to load')
		
	def save_classifier(self):
		'''Save classifier.'''
		
		now = str(datetime.now()).replace(':', '-')
		
		file_opt = options = {}
		options['defaultextension'] = ''
		options['initialfile'] = 'c_' + now[:19] + '.pickle'
		options['filetypes'] = [('pickle file', '.pickle')]
		options['initialdir'] = getcwd() + '\\data'
		options['title'] = 'Save classifier'
		options['parent'] = self.parent
		
		# create dir if not exist
		if not path.exists(options['initialdir']):
			makedirs(options['initialdir'])
		
		file_name = tkFD.asksaveasfilename(**file_opt)
		
		self.text_output.delete('1.0', END)
		if file_name:
			if self.FFF._classifier.save(file_name):
				self.text_output.insert(END, 'Saving classifier successful...' + '\n\n')
				util.debug('saved')
			else:
				self.text_output.insert(END, 'Saving classifier failed...' + '\n\n')
				util.debug('failed to save classifier')
	
	# save and load result
	def load_result(self):
		'''Load classify result.'''
		
		file_opt = options = {}
		options['defaultextension'] = ''		
		options['filetypes'] = [('pickle file', '.pickle')]
		options['initialdir'] = getcwd() + '\\data'
		options['title'] = 'Load Result'
		options['parent'] = self.parent
		
		# create dir if not exist
		if not path.exists(options['initialdir']):
			makedirs(options['initialdir'])
		
		file_name = tkFD.askopenfilename(**file_opt)
		
		if file_name:
			print file_name
			flag, self.FFF._factor_finder = self.FFF._factor_finder.load(file_name)
			self.text_output.delete('1.0', END)
			
			# print to the output text
			if flag:
				util.debug('Loaded')
				self.text_output.insert(END, 'Result loaded...' + '\n\n')

			else:
				self.text_output.insert(END, 'Failed to load result...')
				util.debug('Failed to load result')
	
	def save_result(self):
		'''Save classify result.'''
		
		now = str(datetime.now()).replace(':', '-')
		
		file_opt = options = {}
		options['defaultextension'] = ''
		options['initialfile'] = 'ff_' + now[:19] + '.pickle'
		options['filetypes'] = [('pickle file', '.pickle')]
		options['initialdir'] = getcwd() + '\\data'
		options['title'] = 'Save Result'
		options['parent'] = self.parent
		
		# create dir if not exist
		if not path.exists(options['initialdir']):
			makedirs(options['initialdir'])
		
		file_name = tkFD.asksaveasfilename(**file_opt)
		
		self.text_output.delete('1.0', END)
		if file_name:
			if self.FFF._factor_finder.save(file_name):
				self.text_output.insert(END, 'Saving result successful...' + '\n\n')
				util.debug('saved')
			else:
				self.text_output.insert(END, 'Saving result failed...' + '\n\n')
				util.debug('failed to save result')
		pass

# Run F3 Run
def main():
	root = Tk()
	application = ClassificationForm(root, "F3")
	root.mainloop()

if __name__ == '__main__':
	print 'tes'
	main()