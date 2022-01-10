import regex as re
import cst
import parsing_datafile as parser

def read_column(filename, numCol):  
    """Parse le fichier csv et lire les valeurs de la colonne OriginalTweet
    Args:
        filename: string, nom du fichier en entrée
	numCol: integer, numero de la colonne en entrée 
    Returns:
        Une liste de la colonne OriginalTweet
    """
    lsCols = parser.parse_datafile(filename)
    return lsCols[numCol]

def read_file(filename):
 with open(filename) as f :
   ls = [line.strip('\n') for line in f.readlines()]
 return ls

def camel_case_split(str): 
    words = [[str[0]]]   
    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c)   
    ls = [''.join(word) for word in words]
    newHashtag = ' '.join(ls)
    return newHashtag

def word_break(dictionary, s): 
 result = []
 final_result = ''
 max_l = len(max(dictionary, key=len))
 length = len(s) + 1
 for j in range(1,length):
    i = j - 1
    flag = 0
    ans = []
    x = 0
    # Letting setting x to j - max_l optimization,
    # the code will work even if x is always set to 0
    if j > max_l:
        x = j - max_l
    while(i >= x):
        if s[i:j] in dictionary:
            if i > 0 and result[(i - 1)]:
                    # appending the word to all the valid sentences
                    # formed by the substring ending at i-1
                    temp = list((map(lambda x : x + " "+ s[i:j],\
                    result[(i - 1)])))
                    for elem in temp:
                        ans.append(elem)
                    flag = 2
            else:
                flag = 1
                result.append([s[i:j]])
        i=i-1
    # if the substring does not belong to the
    # dictionary append an empty list to result
    if flag == 0:
        result.append([])
    if flag == 2:
        result.append(ans)
 if s in dictionary:
  result[len(s) - 1].append(s)
 # Printing the result.
 temp = ", result [{}]: "
 for i in range(len(s)):
   print("s:", s[:(i+1)], temp.format(i), result[i])
 # If result[len(s)-1] is empty then the string cannot be 
 # broken down into valid strings
 return final_result.join(result[1])

def remove_hashtags(lsCol):
    """lire les elements de la liste et supprimer les hashtags sans les mots suivis par #
    Args:
        lsCol: liste, liste de la colonne OriginalTweet en entrée
    
    Returns:
        Une liste de la colonne OriginalTweet sans hashtags
    """
    CleanCol = []
    regex1 = r"#([a-zA-Z0-9]+)"
    regex2 = r"#([a-z0-9]+)"
    for i in range(len(lsCol)):
          seperate_word = re.sub(regex1,lambda match: camel_case_split(match.group(1)),lsCol[i])
       #   seperate_word = re.sub(regex2,lambda match: word_break(read_file(cst.DIC), (match.group(1))),lsCol[i])
          CleanCol.append(seperate_word)
    return CleanCol

def remove_urls(lsCol):
    """lire les elements de la liste et supprimer les urls
    Args:
        lsCol: liste, liste de la colonne OriginalTweet en entrée
    
    Returns:
        Une liste de la colonne OriginalTweet sans urls
    """
    CleanCol = []
    for i in range(len(lsCol)):
       CleanCol.append((re.compile(r'https\S+|www\.\S+')).sub(r'', lsCol[i]))
    return CleanCol

def remove_mentions(lsCol):
    """lire les elements de la liste et supprimer les mentions
    Args:
        lsCol: liste, liste de la colonne OriginalTweet en entrée
    
    Returns:
        Une liste de la colonne OriginalTweet sans mentions
    """
    CleanCol = []
    for i in range(len(lsCol)):
       CleanCol.append(re.sub(r'@\w+','',lsCol[i]))
    return CleanCol

def remove_special_caracters(lsCol):
    """Supprime les signes de ponctuation et les caractères spéciaux HTML.
    Args:
        lsCol : liste des éléments à nettoyer
    Returns:
        Une liste d'éléments nettoyés
    """
    regex = "¬[^¬í]|&\w+;|[.;?!,_|:()/]"
    return [re.sub(regex, " ", elt) for elt in lsCol]

def replace_synonyms(string):
    regex = "covid-?0?19|covid-?2019"
    replaced = re.sub(regex, "covid", string)
    regex = "corona virus |coronavir |coronav rus |coronavir s |coronavirus ?\d+"
    replaced = re.sub(regex, "coronavirus ", replaced)
    return replaced


def preprocess(lsCol):
    """Remplace le caractère spécial ¬í et (antislash) x92 par une apostrophe.
    Remplace les autres caractères (antislash) x suivi d'un nombre en hexadécimal et le \n par un espace.
    Remplace les séquences de 2 espaces ou plus par un espace.
    Mets les éléments de lsCol en minuscule et retire les espaces à gauche et droite.
    Args:
        lsCol : liste des éléments à traiter
    Returns:
        Une liste d'éléments traités
    """
    processed = []
    for elt in lsCol:
        apostrophed = re.sub("¬í|\\x92", "'", elt.lower())
        no_newline = apostrophed.replace("\n", " ")
        no_unicode = re.sub(r"[\x80-\xff]", " ", no_newline)
        replaced = replace_synonyms(no_unicode)
        processed.append(re.sub(" {2,}", " ", replaced.strip()))
    return processed


def clean_text(filename):
    """parse le fichier csv et supprime les hashtags, urls et mentions
    Args:
        filename: string, nom du fichier en entrée
    
    Returns:
        Une liste de la colonne OriginalTweet sans hashtags,sans urls et sans mentions
    """
    cleaned = remove_special_caracters(remove_mentions(remove_urls(remove_hashtags(read_column(filename,4)))))
    return preprocess(cleaned)

if __name__ == "__main__":
    print(clean_text(cst.TRAIN))
    
    

