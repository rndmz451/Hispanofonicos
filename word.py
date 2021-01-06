
STRONG_VOWELS = ['a','e','o','á','é','í','ó','ú','ý']

WEAK_VOWELS = ['i','ü','u','y','w']

# It does not include semi-vowels/consonants
FULL_VOWELS = ['a','e','o','á','é','í','ó','ú','ý','i','ü','u']


class vowel:

    def __init__(self, vowel_num, ind, text):
        self.vowel_num = vowel_num
        self.index = ind
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text# + " ---> " + str(self.index) + " ---> " + str(self.vowel_num)

class consonant:
    def __init__(self, ind, text):
        self.index = ind
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text# + " ---> " + str(self.index)

class Syllable:
    def __init__(self, onset, nucleus, coda):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda

    def getIPA(self):
        
        return None


######################################################

######################################################
class Word:
    
    """ self.syllables = []
    self.original = None """

    def __init__(self, text):
        #self.syllables = syllables
        self.original = text
        self.text = text.lower()
        self.syllables = []
        self.nuclei = []
        self.limit = len(self.text)

        self.get_syllables()
        self.get_onsets()
        self.get_codas()
        self.syllables_text()

        print(self.syllables)

    def getIPA(self):
        return None

    def syllables_text(self):
        
        for i in range(len(self.nuclei)):
            current = self.onsets[i] + self.nuclei[i] + self.codas[i] 
            self.syllables.append(current)

    def print_syllables(self):
        
        syllables = []

        for i in range(len(self.nuclei)):
            onset = ""
            nucleus = ""
            coda = ""
            for ii in self.onsets[i]:
                onset += ii.text
            for ii in self.nuclei[i]:
                nucleus += ii.text
            for ii in self.codas[i]:
                coda += ii.text
            
            
            syllables.append(onset + nucleus + coda)
        
        for s in syllables:
            print(s, end='-')
        print()

    
    def isVowel(self, letter):
        return letter in STRONG_VOWELS or letter in WEAK_VOWELS

    def print_nuclei(self):
        for i in self.nuclei:
            print(f"{i}")

    def print_onsets(self):
        for i in self.onsets:
            print(f"{i}")

    def print_codas(self):
        for i in self.codas:
            print(f"{i}")


    def get_syllables(self):
        skip = False
        #print(f"Limit: {self.limit}")

        curr_syllable = []

        curr_vowel_num = 1
        # Beginning of main loop
        for i, letter in enumerate(self.text):

            if skip:
                skip = False
                continue
                
            
            # Case ɸ - last syllable
            if i + 1 == self.limit:
                #print("EOF next")
                if self.isVowel(letter):
                    curr_syllable.append(vowel(1, i, letter))
                    self.nuclei.append(curr_syllable)
                    curr_syllable = []
                    curr_vowel_num = 1
            
            # Individual cases for each case
            else:
                if self.isVowel(letter):
                    #print(letter)

                   
                    if self.case_III(i):
                        curr_syllable.append(vowel(curr_vowel_num, i, letter))
                        self.nuclei.append(curr_syllable)
                        
                        curr_syllable = []
                        curr_vowel_num = 1

                    # LIST A -- strong vowels
                    elif letter in STRONG_VOWELS or (curr_vowel_num == 2 and letter not in ['y', 'w']):

                        # Add two
                        if self.case_V(i):
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            curr_syllable.append(vowel(curr_vowel_num + 1, i + 1, self.text[i+1]))
                            self.nuclei.append(curr_syllable)
                            curr_syllable = []
                            skip = True
                            curr_vowel_num = 1
                        
                        # Case VI
                        else:
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            self.nuclei.append(curr_syllable)
                            curr_syllable = [] 
                            curr_vowel_num = 1
                        # DONE for Case A
                    
                    # B1 
                    elif letter in ['i', 'ü']:
                        if self.case_IV(i):
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            curr_vowel_num = 2
                        
                        # Case VI
                        else:
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            self.nuclei.append(curr_syllable)
                            curr_syllable = []  
                            curr_vowel_num = 1

                    # B2
                    elif letter == "u":
                        if self.case_II(i):
                            continue
                        elif self.case_IV(i):
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            curr_vowel_num = 2
                        # Case VI
                        else:
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            self.nuclei.append(curr_syllable)
                            curr_syllable = []  
                            curr_vowel_num = 1

                    # B3
                    elif letter in ['y', 'w']:
                        
                        if self.case_I(i):
                            if len(curr_syllable) > 0:
                                self.nuclei.append(curr_syllable)
                                curr_syllable = []  
                                curr_vowel_num = 1
                            continue
                        
                        # Case VI
                        else:
                            curr_syllable.append(vowel(curr_vowel_num, i, letter))
                            self.nuclei.append(curr_syllable)
                            curr_syllable = []  
                            curr_vowel_num = 1

    def get_onsets(self):
        """ 
        Get all the possible onsets.
        """
        self.num_syllables = len(self.nuclei)
        self.onsets = []
        print(f"Number of syllables: {self.num_syllables}")

        curr_onset = []
        last_index = 0
        for i, nuc in enumerate(self.nuclei):

            
            # [I] Get first onset
            if i == 0:
                onset_str = self.text[0:nuc[0].index]
                #print(curr_onset)
                for i,c in enumerate(onset_str):
                    curr_onset.append(consonant(i, c))
                    
                self.onsets.append(curr_onset)
                curr_onset = []

                last_index = nuc[len(nuc) - 1].index
                continue

            # [II] Check syllables with no onset 
            if nuc[0].index - 1 == last_index:
                self.onsets.append([])
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue


            

            # [III] Case for 'u'
            index_prev = nuc[0].index - 1
            previous = self.text[index_prev]
            
            if (previous == 'u' and self.text[nuc[0].index - 2] in ['q', 'g']):
                onset_str = self.text[nuc[0].index - 2] + previous
                
                for i,c in enumerate(onset_str, start=nuc[0].index - 2):
                    #print(i)
                    curr_onset.append(consonant(i, c))
                
                self.onsets.append(curr_onset)
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue

            # [IV] Case for all consonants
            if previous not in ['l','r','h']:
                curr_onset.append(consonant(index_prev, previous))
                self.onsets.append(curr_onset)
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue

            index_prev_prev = nuc[0].index - 2
            prev_previous = self.text[index_prev_prev]
            # [V] Case for all consonants
            if self.isVowel(prev_previous):
                curr_onset.append(consonant(index_prev, previous))
                self.onsets.append(curr_onset)
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue
                
            # [VI] Case for double
            if ((previous == 'h' and prev_previous == 'c') or
                (previous == 'r' and prev_previous in ['b','c','d','f','g','r']) or
                (previous == 'l' and prev_previous in ['b','c','d','f','g','l'])):
                
                curr_onset.append(consonant(index_prev_prev, prev_previous))
                curr_onset.append(consonant(index_prev, previous))
                
                self.onsets.append(curr_onset)
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue

            else:
                self.onsets.append([])
                curr_onset = []
                last_index = nuc[len(nuc) - 1].index
                continue

        #self.print_onsets()

    def get_codas(self):
        self.codas = []
        curr_coda = []
        len_nuc = len(self.nuclei)
        for ind in range(len_nuc):
            # /I/ Case for the last
            len_last_n = len(self.nuclei[ind])
            last = self.nuclei[ind][len_last_n - 1].index
            if ind == (len_nuc - 1):
                coda = self.text[last + 1 :]
                #print(coda)
                for  i, c in enumerate(coda, start=last):
                    curr_coda.append(consonant(i, c))
                
                self.codas.append(curr_coda)
                curr_coda = []
                continue
            
            first = self.onsets[ind + 1][0].index
            #print(f"::: Last {last} ::: First {first} ")
            
            coda = self.text[last + 1: first]
            for  i, c in enumerate(coda, start=last):
                curr_coda.append(consonant(i, c))
            
            self.codas.append(curr_coda)
            curr_coda = []


    def __str__(self):
        return self.original


    def __repr__(self):
        return self.original

    ## CASES ##

    def case_I(self, curr_ind):
        next_letter = self.text[curr_ind + 1]
        return self.isVowel(next_letter)

    def case_II(self, curr_ind):
        
        if curr_ind-1 < 0:
            return False
        prev = self.text[curr_ind-1]
        next = self.text[curr_ind+1]
        

        if prev in ['q', 'g'] and next in ['e', 'é', 'i', 'í']:
            return True 
        return False

    def case_III(self, curr_ind):
        next_letter = self.text[curr_ind + 1]

        return not self.isVowel(next_letter)

    def case_IV(self, curr_ind):
        next_letter = self.text[curr_ind + 1]

        return self.isVowel(next_letter)


    def case_V(self, curr_ind):
        next_letter = self.text[curr_ind + 1]
        
        if next_letter in WEAK_VOWELS:
            # Check if after next exists
            if self.limit != curr_ind + 2:
                after_next_letter = self.text[curr_ind + 2]
                if not self.isVowel(after_next_letter):
                    return True

            # OK if next is last
            else:
                return True 

        return False 

