#!/F3/core/classification_form.py
# This file contain form for classification
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-28

import random
from Tkinter import *
from core.util import *
from F3 import *
import core.tweet_model as tm

class ClassificationForm():
	"""GUI form for classification."""

	def __init__(self, parent, title):
		"""Init function for ClassificationForm."""

		self.parent = parent
		self.parent.title(title)
		self.parent.protocol("WM_DELETE_WINDOW", self.exit)
		self.init_components()
		self.FFF = F3()


	def init_components(self):
		"""Initialize components."""

		# Main frame
		main_frame = Frame(self.parent, bd = 10)
		main_frame.pack(fill = BOTH, expand = YES)

		# Label User Input
		Label(main_frame, text = "Parameter").grid(row = 0, column = 0, columnspan = 2, sticky = W, padx = 5, pady = 5)

		# Label kata kunci
		Label(main_frame, text = "Kata Kunci").grid(row = 1, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry keyword
		self.ent_keyword = Entry(main_frame)
		self.ent_keyword.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_keyword.insert(END, 'bad dum tss')

		# label fold
		Label(main_frame, text = "Fold").grid(row = 2, column = 0, sticky = W, padx = 5, pady = 5)

		# Entry fold
		self.ent_fold = Entry(main_frame)
		self.ent_fold.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
		self.ent_fold.insert(END, '10')

		# label num_tweet
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

		# show tweet
		self.show_tweet_val = IntVar()
		self.show_tweet_cb = Checkbutton(main_frame, text = "Show Tweet ?",  variable = self.show_tweet_val, onvalue = 1, offvalue = 0)
		self.show_tweet_cb.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = W)

		# Button get accuracy cross validation
		self.btn_cross_validation = Button(main_frame, text = 'Hitung Akurasi', command = self.get_accuracy_cross_validation)
		self.btn_cross_validation.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = W+E, columnspan = 2)

		# Button training
		self.btn_train_classifier = Button(main_frame, text = 'Train', command = self.train_classifier)
		self.btn_train_classifier.grid(row = 8, column = 0, padx = 5, pady = 5, sticky = W+E, columnspan = 2)

		# Button classify
		self.btn_classify = Button(main_frame, text = 'Classify', command = self.classify)
		self.btn_classify.grid(row = 9, column = 0, padx = 5, pady = 5, sticky = W+E, columnspan = 2)

		# Label preprocess
		Label(main_frame, text = "Preprocess Options").grid(row = 0, column = 2, sticky = W, padx = 5, pady = 5)

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
		self.convert_emoticon_cb.grid(row = 7, column = 2, padx = 5, pady = 5, sticky = W)
		self.remove_punctuation_string_cb.grid(row = 8, column = 2, padx = 5, pady = 5, sticky = W)
		self.convert_word_cb.grid(row = 9, column = 2, padx = 5, pady = 5, sticky = W)
		self.remove_stop_words_cb.grid(row = 10, column = 2, padx = 5, pady = 5, sticky = W)
		self.convert_negation_cb.grid(row = 11, column = 2, padx = 5, pady = 5, sticky = W)

		# Label output
		Label(main_frame, text = "Output").grid(row = 0, column = 3, sticky = W, padx = 5, pady = 5)

		# output text
		self.text_output = Text(main_frame, wrap = WORD)
		self.text_output.grid(row = 1, column = 3, padx = 5, pady = 5, rowspan = 11, sticky = W+E+N+S)


	def exit(self, event = None):
		"""Exit form application."""

		self.parent.destroy()

	def get_accuracy_cross_validation(self):
		keyword = self.ent_keyword.get()
		self.dict_param = {}
		try:
			fold = int(self.ent_fold.get())
			num_tweet = int(self.ent_num_tweet.get())
			random_seed = int(self.ent_random_seed.get())
			min_occur = int(self.ent_min_occur.get())

			# parameter
			self.dict_param['fold_case'] = self.fold_case_val.get()
			self.dict_param['remove_RT'] = self.remove_rt_val.get()
			self.dict_param['remove_hashtag'] = self.remove_hashtag_val.get()
			self.dict_param['remove_username'] = self.remove_username_val.get()
			self.dict_param['convert_number'] = self.convert_number_val.get()
			self.dict_param['clean_number'] = self.clean_number_val.get()
			self.dict_param['convert_emoticon'] = self.convert_emoticon_val.get()
			self.dict_param['remove_punctuation_string'] = self.remove_punctuation_string_val.get()
			self.dict_param['convert_word'] = self.convert_word_val.get()
			self.dict_param['remove_stop_words'] = self.remove_stop_words_val.get()
			self.dict_param['convert_negation'] = self.convert_negation_val.get()

		except Exception, e:
			raise e
			debug(str(e))

		dev_tweets = tm.get_dev_data()
		accuration = self.FFF.get_accuracy_cross_validation(dev_tweets, num_tweet, fold, keyword, random_seed, min_occur, self.dict_param)
		# print self.dict_param
		self.text_output.delete('1.0', END)
		self.text_output.insert(END, 'Parameter : ' + '\n')
		
		self.text_output.insert(END, 'Fold Case : ' + str(bool(self.dict_param['fold_case']))  + '\n')
		self.text_output.insert(END, 'Remove RT : ' + str(bool(self.dict_param['remove_RT'])) +'\n')
		self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(self.dict_param['remove_hashtag'])) + '\n')
		self.text_output.insert(END, 'Remove Username : ' + str(bool(self.dict_param['remove_username']))  + '\n')
		self.text_output.insert(END, 'Convert Number : ' + str(bool(self.dict_param['convert_number'])) + '\n')
		self.text_output.insert(END, 'Clean Number : ' + str(bool(self.dict_param['clean_number'])) + '\n')
		self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(self.dict_param['convert_emoticon'])) + '\n')
		self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(self.dict_param['remove_punctuation_string'])) + '\n')
		self.text_output.insert(END, 'Convert Word : ' + str(bool(self.dict_param['convert_word'])) + '\n')
		self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(self.dict_param['remove_stop_words'])) + '\n')
		self.text_output.insert(END, 'Convert Negation : ' + str(bool(self.dict_param['convert_negation'])) + '\n\n')

		self.text_output.insert(END, 'Fold : ' + str(fold) + '\n')
		self.text_output.insert(END, 'Banyak Tweet : ' + str(num_tweet) + '\n')
		self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
		self.text_output.insert(END, 'Minimal Kemunculan : ' + str(min_occur) + '\n\n')
		self.text_output.insert(END, 'Akurasi : ' + str(accuration) + '\n')

	def train_classifier(self):
		keyword = self.ent_keyword.get()
		self.dict_param = {}
		try:
			fold = int(self.ent_fold.get())
			num_tweet = int(self.ent_num_tweet.get())
			random_seed = int(self.ent_random_seed.get())
			min_occur = int(self.ent_min_occur.get())

			# parameter
			self.dict_param['fold_case'] = self.fold_case_val.get()
			self.dict_param['remove_RT'] = self.remove_rt_val.get()
			self.dict_param['remove_hashtag'] = self.remove_hashtag_val.get()
			self.dict_param['remove_username'] = self.remove_username_val.get()
			self.dict_param['convert_number'] = self.convert_number_val.get()
			self.dict_param['clean_number'] = self.clean_number_val.get()
			self.dict_param['convert_emoticon'] = self.convert_emoticon_val.get()
			self.dict_param['remove_punctuation_string'] = self.remove_punctuation_string_val.get()
			self.dict_param['convert_word'] = self.convert_word_val.get()
			self.dict_param['remove_stop_words'] = self.remove_stop_words_val.get()
			self.dict_param['convert_negation'] = self.convert_negation_val.get()

		except Exception, e:
			raise e
			debug(str(e))

		dev_tweets = tm.get_dev_data()
		self.FFF.train_classifier(dev_tweets, num_tweet, keyword, self.dict_param, min_occur)

		self.text_output.delete('1.0', END)
		self.text_output.insert(END, 'Training Classifier' + '\n')
		self.text_output.insert(END, 'Parameter : ' + '\n')
		
		self.text_output.insert(END, 'Fold Case : ' + str(bool(self.dict_param['fold_case']))  + '\n')
		self.text_output.insert(END, 'Remove RT : ' + str(bool(self.dict_param['remove_RT'])) +'\n')
		self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(self.dict_param['remove_hashtag'])) + '\n')
		self.text_output.insert(END, 'Remove Username : ' + str(bool(self.dict_param['remove_username']))  + '\n')
		self.text_output.insert(END, 'Convert Number : ' + str(bool(self.dict_param['convert_number'])) + '\n')
		self.text_output.insert(END, 'Clean Number : ' + str(bool(self.dict_param['clean_number'])) + '\n')
		self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(self.dict_param['convert_emoticon'])) + '\n')
		self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(self.dict_param['remove_punctuation_string'])) + '\n')
		self.text_output.insert(END, 'Convert Word : ' + str(bool(self.dict_param['convert_word'])) + '\n')
		self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(self.dict_param['remove_stop_words'])) + '\n')
		self.text_output.insert(END, 'Convert Negation : ' + str(bool(self.dict_param['convert_negation'])) + '\n\n')

		self.text_output.insert(END, 'Banyak Tweet : ' + str(num_tweet) + '\n')
		# self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
		self.text_output.insert(END, 'Minimal Kemunculan : ' + str(min_occur) + '\n\n')
		self.text_output.insert(END, 'Train : ' + str(self.FFF._classifier.trained) + '\n')

	def classify(self):
		self.text_output.delete('1.0', END)
		if not self.FFF._classifier.trained:
			self.text_output.insert(END, 'Gagal mengklasifikasikan, belum ditraining' + '\n')	
		else:
			keyword = self.ent_keyword.get()
			self.dict_param = {}
			try:
				fold = int(self.ent_fold.get())
				num_tweet = int(self.ent_num_tweet.get())
				random_seed = int(self.ent_random_seed.get())
				min_occur = int(self.ent_min_occur.get())

				# parameter
				self.dict_param['fold_case'] = self.fold_case_val.get()
				self.dict_param['remove_RT'] = self.remove_rt_val.get()
				self.dict_param['remove_hashtag'] = self.remove_hashtag_val.get()
				self.dict_param['remove_username'] = self.remove_username_val.get()
				self.dict_param['convert_number'] = self.convert_number_val.get()
				self.dict_param['clean_number'] = self.clean_number_val.get()
				self.dict_param['convert_emoticon'] = self.convert_emoticon_val.get()
				self.dict_param['remove_punctuation_string'] = self.remove_punctuation_string_val.get()
				self.dict_param['convert_word'] = self.convert_word_val.get()
				self.dict_param['remove_stop_words'] = self.remove_stop_words_val.get()
				self.dict_param['convert_negation'] = self.convert_negation_val.get()

			except Exception, e:
				raise e
				debug(str(e))
			
			test_data = tm.get_test_data(keyword)
			random.seed(random_seed)
			random.shuffle(test_data)
			self.list_tweet = self.FFF.classify_tweets(test_data, keyword, self.dict_param, num_tweet)

			self.text_output.delete('1.0', END)
			self.text_output.insert(END, 'Hasil Klasifikasi' + '\n')
			self.text_output.insert(END, 'Parameter : ' + '\n')
			self.text_output.insert(END, 'Fold Case : ' + str(bool(self.dict_param['fold_case']))  + '\n')
			self.text_output.insert(END, 'Remove RT : ' + str(bool(self.dict_param['remove_RT'])) +'\n')
			self.text_output.insert(END, 'Remove Hashtag : ' + str(bool(self.dict_param['remove_hashtag'])) + '\n')
			self.text_output.insert(END, 'Remove Username : ' + str(bool(self.dict_param['remove_username']))  + '\n')
			self.text_output.insert(END, 'Convert Number : ' + str(bool(self.dict_param['convert_number'])) + '\n')
			self.text_output.insert(END, 'Clean Number : ' + str(bool(self.dict_param['clean_number'])) + '\n')
			self.text_output.insert(END, 'Convert Emoticon : ' + str(bool(self.dict_param['convert_emoticon'])) + '\n')
			self.text_output.insert(END, 'Remove Punctuation : ' + str(bool(self.dict_param['remove_punctuation_string'])) + '\n')
			self.text_output.insert(END, 'Convert Word : ' + str(bool(self.dict_param['convert_word'])) + '\n')
			self.text_output.insert(END, 'Remove Stop Word : ' + str(bool(self.dict_param['remove_stop_words'])) + '\n')
			self.text_output.insert(END, 'Convert Negation : ' + str(bool(self.dict_param['convert_negation'])) + '\n\n')

			self.text_output.insert(END, 'Keyword : ' + keyword + '\n')
			self.text_output.insert(END, 'Banyak Tweet : ' + str(num_tweet) + '\n')
			self.text_output.insert(END, 'Random Seed : ' + str(random_seed) + '\n')
			# self.text_output.insert(END, 'Minimal Kemunculan : ' + str(min_occur) + '\n\n')
			# self.text_output.insert(END, 'Train : ' + str(self.FFF._classifier.trained) + '\n')
			
			# print (self.list_tweet)

			self.show_tweet = self.show_tweet_val.get()
			list_sentiment = []
			if self.show_tweet == 1:
				for t in self.list_tweet:
					self.text_output.insert(END, 'Tweet : ' + str(t.get_normal_text()) + '\n')
					self.text_output.insert(END, 'Sentiment : ' + str(t.sentiment) + '\n\n')
					list_sentiment.append(t.sentiment)
			else:
				for t in self.list_tweet:
					# self.text_output.insert(END, 'Tweet : ' + str(t.get_normal_text()) + '\n')
					# self.text_output.insert(END, 'Sentiment : ' + str(t.sentiment) + '\n')
					list_sentiment.append(t.sentiment)

			self.text_output.insert(END, '\n')
			self.text_output.insert(END, 'Result : \n')
			self.text_output.insert(END, 'Positif :'+ str(list_sentiment.count(1)) + ' \n')
			self.text_output.insert(END, 'Netral :'+ str(list_sentiment.count(0)) + ' \n')
			self.text_output.insert(END, 'Negatif :'+ str(list_sentiment.count(-1)) + ' \n')

def main():
	root = Tk()
	application = ClassificationForm(root, "F3")
	root.mainloop()

if __name__ == '__main__':
	print 'tes'
	main()