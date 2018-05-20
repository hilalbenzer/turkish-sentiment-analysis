import operator, ast
import Util

dictionary = Util.read_file("dictionary.txt")
dictionary_x = sorted(ast.literal_eval(dictionary).items(), key=operator.itemgetter(1), reverse=True)
Util.write_file("dictionary_sorted", dictionary_x)