from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk.corpus import wordnet
import re
from englisttohindi.englisttohindi import EngtoHindi
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import tnt
def get_prepositions():
    prepositions = []
    for synset in wordnet.all_synsets(pos='r'):
        if synset.lexname() == 'Adverb':
            prepositions.append(synset.lemmas()[0].name())
    return prepositions

# nltk.download('punkt')
# nltk.download('wordnet')

def is_valid_plural(word):
    lemma = wordnet.morphy(word, wordnet.NOUN)
    if lemma is None:
        return False
    singular_form = wordnet.morphy(word, wordnet.NOUN)
    return singular_form is not None and singular_form != word

def replace_plurals(line):
    words = nltk.word_tokenize(line)
    singular_words = []
    for word in words:
        if is_valid_plural(word):
            lemma = wordnet.morphy(word, wordnet.NOUN)
            singular_words.append(lemma)
        else:
            singular_words.append(word)
    return ' '.join(singular_words)
def spell_check(text):
    spell = SpellChecker()
    words = text.split()
    misspelled = spell.unknown(words)
    corrected_text = ''
    for word in words:
        if word is not None:
            if word.lower() in misspelled:
                pos = nltk.pos_tag([word])[0][1]
                if not pos.startswith('NN') and not pos.startswith('SYM') and not pos.startswith('``') and not pos.startswith("''"):
                    if spell.correction(word) is not None:
                        corrected_text += spell.correction(word) + ' '
                else:
                    corrected_text += word + ' '
            else:
                corrected_text += word + ' '
    return corrected_text.strip()
def split_sentence(sentence):
    conjunctions = ['and', 'but', 'or', 'nor', 'yet', 'so', 'either', 'neither', 'not only', 'but also', 'as', 'both', 'whether','after','although','as soon as','because','before','by the time','in case','now that','since','unless','when','whether or not','while']
    pattern = r'\b(' + '|'.join(conjunctions) + r')\b'
    split_sentences = re.split(pattern, sentence, flags=re.IGNORECASE)
    return split_sentences
from translate import Translator
def translate_comments(c_code, target_language='hi'):
    translator = Translator(to_lang=target_language)

    def translate_comment(match):
        comment = match.group(1)
        translated_comment = translator.translate(comment.strip())
        return match.group(0).replace(comment, translated_comment)

    # Match both // and /* */ style comments
    pattern = r'(\/\/[^\n]*|\/\*.*?\*\/)'
    translated_code = re.sub(pattern, translate_comment, c_code, flags=re.DOTALL)

    return translated_code


def convert_verb_forms(sentence):
    lemmatizer = WordNetLemmatizer()
    words=[]
    if not sentence:
        words=(nltk.word_tokenize(''))
    else:
        words=(nltk.word_tokenize(sentence))
    converted_sentence = []
    for word in words:
        pos = nltk.pos_tag([word])[0][1]
        if pos.startswith('VB'):
            converted_word = lemmatizer.lemmatize(word, pos='v')
            converted_sentence.append(converted_word)
        else:
            converted_sentence.append(word)
    return ' '.join(converted_sentence)
def helper1(sentence):
    text=nltk.sent_tokenize(sentence)
    tokens = []
    if not text:
        tokens.append(nltk.word_tokenize(''))
    else:
        for i in text:
            tokens.append(nltk.word_tokenize(i))
#     print(tokens)
    tagged_words=[]
    if tokens!=[]:
        tagged_words = nltk.pos_tag(tokens[0])
    # print(tagged_words)
    not_req = {'a', 'an', 'the', 'is', 'am', 'are', 'was', 'were'}
    conjunctions = ['and', 'but', 'or', 'nor', 'for', 'yet', 'so', 'either', 'neither', 'not only', 'but also', 'as', 'both', 'whether','after','although','as soon as','because','before','by the time','in case','now that','since','unless','when','whether or not','while']
    prepositions = get_prepositions()
    stop_words=set(stopwords.words('english'))
    filtered_sentence = []
    for i in tagged_words:
        if not i[0].lower() in not_req and not i[0].lower() in conjunctions and not i[0].lower() in stop_words and not i[0].lower() in prepositions:
            filtered_sentence.append(i)
#     print(filtered_sentence)
    verb_index = 0
    v=0
#     print(filtered_sentence)
    for i in range(len(filtered_sentence)):
#         print(filtered_sentence[i])
        if str(filtered_sentence[i][1]).startswith('V'):
            verb_index=i
            for k in filtered_sentence[verb_index+1:]:
                if k[1].startswith('V'):
                    v+=1
    return [verb_index,v,filtered_sentence]
def helper2(verb_index,v,abc):
    if verb_index is not None:
        # Reorder the words to SOV form
        reordered_words=[]
        for i in abc[:verb_index]:
            reordered_words.append(i)
        for i in abc[verb_index+v+1:]:
            reordered_words.append(i)
        for i in (abc[verb_index:verb_index+v+1]):
            reordered_words.append(i)
#         print(reordered_words)
        # Extract the words from the reordered list
        reordered_sentence = ""
        for i in reordered_words:
            reordered_sentence+=str(i[0])+' '
        return reordered_sentence
    return abc
def helper3(sentence):
    text=nltk.sent_tokenize(sentence)
    tokens = []
    if not text:
        tokens.append(nltk.word_tokenize(''))
    else:
        for i in text:
            tokens.append(nltk.word_tokenize(i))
#     print(tokens)
    tagged_words=[]
    if tokens!=[]:
        tagged_words = nltk.pos_tag(tokens[0])
#     print(tagged_words)
    verb_index = 0
    v=0
    for i in range(len(tagged_words)):
#         print(tagged_words[i])
        if str(tagged_words[i][1]).startswith('V'):
            verb_index=i
            for k in tagged_words[verb_index+1:]:
                if k[1].startswith('V'):
                    v+=1
    return [verb_index,v,tagged_words]
def find_variables(code):
    # Match variable declarations (e.g., int x;, float y;, char c;)
    variables = re.findall(r'\b(int|float|double|char|short|long)\s+(\w+)\b\s*;', code)
    # Match variable assignments (e.g., x = 10;, y = 3.14;, c = 'A';)
    assignments = re.findall(r'\b(\w+)\s*=\s*.*?;', code)
    # Combine both variable declarations and assignments
    all_variables = [v[1] for v in variables] + assignments
    return all_variables
def find_data_types(code):
    return re.findall(r'\b(int|float|double|char|void| )\b', code)

def find_udt(code):
    udt_names = []
    struct_names = re.findall(r'\bstruct\s+(\w+)\b', code)
    union_names = re.findall(r'\bunion\s+(\w+)\b', code)
    enum_names = re.findall(r'\benum\s+(\w+)\b', code)
    
    udt_names.extend(struct_names)
    udt_names.extend(union_names)
    udt_names.extend(enum_names)

    return udt_names

def find_function_names(code):
    return re.findall(r'\b(\w+)\s+(\w+)\s*\([^)]*\)\s*\{', code)
def remove_c_data_types(input_list):
    c_data_types = ['int', 'float', 'double', 'char', 'void']
    filtered_list = []
    for i in input_list:
        if type(i)==tuple or type(i)==tuple:
            for item in i:
                if item not in c_data_types:
                    filtered_list.append(item)
        else:
            if i not in c_data_types:
                filtered_list.append(i)
    return filtered_list
variables,data_types,udt,function_names=[],[],[],[]
def find_anonymous(code):
    global variables,data_types,udt,function_names
    variables.append(find_variables(code))
    data_types.append(find_data_types(code))
    udt.append(find_udt(code))
    function_names.append(find_function_names(code))    
def svo_to_sov(text):
    paragraphs = text.split('\n')  # Split text into paragraphs
    transformed_paragraphs = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():  # Skip empty lines
            transformed_paragraphs.append(paragraph)
            continue
        
        sentence = convert_verb_forms(paragraph)
        sentence_corrected = spell_check(sentence)
        final_sentence = replace_plurals(sentence_corrected)
        sent1 = split_sentence(final_sentence)
        final_sent = ""
        for i in sent1:        
            L = helper1(i)
            final_sent += helper2(L[0], L[1], L[2])
        line = remove_punctuation(final_sent)
        transformed_paragraphs.append(line)
    
    return '\n'.join(transformed_paragraphs)
c_keywords_in_hindi = {
    "auto": "स्वचालित",
    "break": "विघटन",
    "case": "मामला",
    "char": "वर्ण",
    "const": "धारित",
    "continue": "जारी",
    "default": "मूल",
    "do": "करो",
    "double": "दोहरा",
    "else": "अन्यथा",
    "enum": "संख्यामला",
    "extern": "बाह्य",
    "float": "लघु",
    "for": "के लिए",
    "goto": "जाओ",
    "if": "यदि",
    "int": "पूर्णांक",
    "long": "लम्बा",
    "register": "रजिस्टर",
    "return": "वापसी",
    "short": "लघु",
    "signed": "संकेतित",
    "sizeof": "आकार",
    "static": "स्थिर",
    "struct": "संरचना",
    "switch": "परिवर्तन",
    "typedef": "पूर्वनिर्धारित",
    "union": "संघ",
    "unsigned": "असंकेतित",
    "void": "शून्य",
    "volatile": "अस्थिर",
    "while": "जबकि "
}
def svo_to_sov2(text):
    if '{' in text and '}' in text:
        find_anonymous(sent)
        return text
    paragraphs = text.split('\n')  # Split text into paragraphs
    transformed_paragraphs = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():  # Skip empty lines
            transformed_paragraphs.append(paragraph)
            continue
    sentence = convert_verb_forms(paragraph)
    sentence_corrected = spell_check(sentence)
    final_sentence = replace_plurals(sentence_corrected)
    sent1 = split_sentence(final_sentence)
    final_sent = ""
    for i in sent1:        
        L = helper3(i)
        final_sent += helper2(L[0], L[1], L[2])
    line = remove_punctuation(final_sent)
    transformed_paragraphs.append(line)
    
    return '\n'.join(transformed_paragraphs)
def e2h(sentence):
    res = EngtoHindi(sentence)
    translation = res.convert
    return translation if translation else ''

def process_sentence(sentence):
    split_sentences = re.split(r';(?=(?:(?:[^"]*"){2})*[^"]*$)', sentence)
    translated_sentences = [e2h(s.strip()) for s in split_sentences]
    non_empty_translations = [t for t in translated_sentences if t]
    if not non_empty_translations:
        return ''
    return ' '.join(non_empty_translations)
def hindi_pos_tag(sentence):
    words = word_tokenize(sentence)
    pos_tagger = tnt.TnT()
    pos_tagger.train(nltk.corpus.indian.tagged_sents('hindi.pos'))
    pos_tags = pos_tagger.tag(words)
    tagged=' '.join([f"{word} ({tag})" for word,tag in pos_tags])
    return tagged
def separate(sentence):
    L=[]
    s=0
    if sentence[0]!='#':
        s=sentence.find('#')
        L.append(sentence[:s])
    str1=sentence[::-1]
    if str1[0]!='}':
        s2=str1.find('}')
        s1=str1[:s2]
        a=(str1[s2:])
        L.append(a[::-1])
        if s!=0:
            s3=str1.find('#')
            a=str1[s3:s2]
            L.append(a[::-1])
        else:
            a=str1[:s2]
            L.append(a[::-1])
    return L

def replace_reserved_words(word):
    c_keywords = ["auto", "break", "case", "char", "const", "continue", "default", "do","double",
                  "else","enum", "extern", "float", "for", "goto", "if", "int","long","register",
                  "return", "short","signed", "sizeof", "static", "struct","switch","typedef",
                  "union", "unsigned", "void","volatile", "while", "NULL", "TRUE", "FALSE",
                  "printf", "scanf", "malloc", "free", "sizeof", "strcpy", "strcat", "strcmp", "strlen"]
    if word in c_keywords:
        return f"{word}()"
    else:
        return word
def main(sentence):
    global c
    if '{' and '}' in sentence:
        L1=separate(sentence)
        for i in L1:
            if '{' and '}' in i:
                text=translate_comments(i)
                find_anonymous(i)
            else:
                reordered_sentence = svo_to_sov2(i)
                output_sentence = svo_to_sov(sentence)
                text=process_sentence(reordered_sentence)
                word=nltk.word_tokenize(text)
                translated=[]
                for i in word:
                    for key,val in c_keywords_in_hindi.items():
                        if val==i:
                            translated.append(key)
                        else:
                            translated.append(i)
                text=e2h(text)
        return []
    else:
        reordered_sentence = svo_to_sov2(sentence)
        output_sentence = svo_to_sov(sentence)
        text=process_sentence(reordered_sentence)
        text=e2h(text)
    return [sentence,reordered_sentence,output_sentence]
def main2(sentence):
    global c
    if '{' and '}' in sentence:
        L1=separate(sentence)
        for i in L1:
            if '{' and '}' in i:
                text=translate_comments(i)
                find_anonymous(i)
            else:
                reordered_sentence = svo_to_sov2(i)
                output_sentence = svo_to_sov(sentence)
                text=process_sentence(reordered_sentence)
                word=nltk.word_tokenize(text)
                translated=[]
                for i in word:
                    for key,val in c_keywords_in_hindi.items():
                        if val==i:
                            translated.append(key)
                        else:
                            translated.append(i)
        return []
    else:
        reordered_sentence = svo_to_sov2(sentence)
        output_sentence = svo_to_sov(sentence)
        text=process_sentence(reordered_sentence)
    return (reordered_sentence,output_sentence,text)
def main3(text):
    L1,L2,L3=[],[],[]
    L=nltk.sent_tokenize(text)
    for i in L:
        x,y,z=main2(i)
        L1.append(x)
        L2.append(y)
        L3.append(z)
    print(L1,L2,L3)
    reordered_sentence='\n'.join(L1)
    output_sentence='\n'.join(L2)
    hindi_sentence='\n'.join(L3)
    return (reordered_sentence,output_sentence,hindi_sentence)
        
def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )
def is_code(line):
    pattern = r'^\s*(?:#include|typedef|struct|enum|union|int|float|double|char|void|if|else|for|while|do|switch|case|break|continue|return)\b'
    return re.match(pattern, line)
import string
def remove_punctuation(line):
    res = line.replace('. ','')
    res1 = res.replace(',','')
    result = res1.replace(', ','')
    return result
import re
def remove_unnecessary(input_list):
    unique_list = []
    for i in input_list:
        for x in i:
            if x not in unique_list and x!=' ':
                unique_list.append(x)
    return unique_list
def convert_sov_to_standard(source_code):
    pattern = r'(/\*.*?\*/)'
    comments = re.findall(pattern, source_code, re.DOTALL)
    placeholder = '<comment_placeholder>'
    source_code_with_placeholders = re.sub(pattern, placeholder, source_code, flags=re.DOTALL)
    lines = source_code_with_placeholders.split('\n')
    converted_lines = []
    comment_index = 0
    for line in lines:
        if placeholder in line:
            line = line.replace(placeholder, comments[comment_index], 1)
            comment_index += 1
        converted_lines.append(line)
    converted_source_code = '\n'.join(converted_lines)
    return converted_source_code

def find_user_declared(sent):
    global variables,data_types,udt,function_names
    a=0
    for i in sent.split():
        if i in variables:
            sent.replace(" "+i+" ","variable "+i)
        elif i in data_types:
            sent.replace(" "+i+" ","data type "+i)
        elif i in udt:
            sent.replace(" "+i+" ","User Defined Type "+i)
        elif i in function_names:
            sent.replace(" "+i+" ","Function "+i+"()")
        else:
            a=1
    return sent

def clean_string(input_str):
    # Remove non-XML-compatible characters
    cleaned_str = ''.join(c for c in input_str if valid_xml_char_ordinal(c))
    return cleaned_str

def write(output_filename):
    global variables,data_types,udt,function_names
    variables = remove_unnecessary(variables)
    data_types = remove_unnecessary(data_types)
    udt = remove_unnecessary(udt)
    function_names = remove_unnecessary(function_names)
    variables = remove_c_data_types(variables)
    udt = remove_c_data_types(udt)
    function_names = remove_c_data_types(function_names)
    with open(output_filename, 'w') as file:
        file.write("Variables: " + str(variables) + "\n")
        file.write("Data Types: " + str(data_types) + "\n")
        file.write("User Defined Types: " + str(udt) + "\n")
        file.write("Function Names: " + str(function_names) + "\n")
print(main2("Hello I am Amogh"))
