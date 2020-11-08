# Imports for Statistics Calculator
import xml.dom.minidom
import re
from database_connector import Database
import logger_mod


# calculation of statistics for all books entering the directory
class StatisticsCalculator:
    def calculate_book_statistic(self, input_file):  # collection of general statistics for all incoming books
        database = Database()
        print('Calculate statistics for ' + input_file)
        logger_mod.logging.info('Calculate statistics for ' + input_file)
        doc = xml.dom.minidom.parse(input_file)

        p = doc.getElementsByTagName("p")

        count_p = 0
        count_p_w = 0
        count_text = 0
        count_word = 0
        upperl = 0
        lowercasel = 0
        count_low = 0
        count_upp = 0

        for text in p:
            alltext = " ".join(z.nodeValue for z in text.childNodes if z.nodeType == z.TEXT_NODE)

            p_t = str(alltext)  # change type to string
            p_t_new = re.findall(r'\b[a-zA-Zа-яА-Я]{1,15}\b', p_t)
            #print(p_t)
            #print(p_t_new)
            for x in range(len(p_t)):
                if p_t[x].isalpha() is True:  # if the symbol is a letter, we count with accumulation
                    count_text += 1
                count_p += count_text  # add a text variable between paragraphs to the variable for counting paragraphs
                count_text = 0  # and before the new iteration we nullify the variable

            #word_text = p_t_new.split()  # for words count we divided text on words

            for w in range(len(p_t_new)):
                if p_t_new[w].istitle() is True:
                    upperl += 1

                elif p_t_new[w].islower() is True:
                    lowercasel += 1
                count_low += lowercasel
                count_upp += upperl

                count_word += 1
                count_p_w += count_word
                count_word = 0
                upperl = 0
                lowercasel = 0
                #print(w)

        bookt = doc.getElementsByTagName("book-title")

        for title in bookt:
            pass
        book_name = "".join(t.nodeValue for t in title.childNodes if t.nodeType == t.TEXT_NODE)

        print("Book name:", book_name)
        print("Paragraph quantity:" "%d" % p.length)
        print("Letters quantity:", count_p)
        print("Words quantaty:", count_p_w)
        print("Words with Capital letter:", count_upp)
        print("Words in lowercase:", count_low)
        database.add_book_statistics(book_name, p.length, count_p_w, count_p, count_upp, count_low)


    def calculate_book_word_count(self, book_id, input_file):  # collection information for each book in the directory
        database = Database()
        print('Calculate word counts for ' + input_file)

        doc = xml.dom.minidom.parse(input_file)
        #print(doc.nodeName)
        #print(doc.firstChild.tagName)

        p = doc.getElementsByTagName("p")

        frequency = {}
        frequency_l = {}

        for text in p:
            alltext = " ".join(z.nodeValue for z in text.childNodes if z.nodeType == z.TEXT_NODE)
            p_t = str(alltext)  # меняем тип на строковый

            # text_string = p_t.lower()
            match_pattern = re.findall(r'\b[a-zA-Zа-яА-Я]{1,15}\b', p_t)

            for word in match_pattern:
                if word.isupper() is True:
                    ct = word.lower()
                    count_upp = frequency.get(ct, 0)
                    frequency[ct] = count_upp + 1
                else:
                    dt = word.lower()
                    count_i = frequency_l.get(dt, 0)
                    frequency_l[dt] = count_i + 1
        #print(frequency)
        #print(frequency_l)
        database.add_book_word_counts(book_id, frequency_l, frequency)

        return
