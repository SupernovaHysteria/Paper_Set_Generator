import random
import sys
import math

def dispdict(di):
    for key in di:
        print(key,':',di[key])

def get_set_number(max_sets):
    sets = 4
    #sets = int(input('Enter the number of sets you want to generate : '))
    if sets>max_sets:
        print('Limit exceeded, please enter a smaller number')
        return(get_set_number(max_sets))
    else:
        print('Accepted')
        return sets


def get_answer_key_info():
    file  = open('AK.txt','r')
    raw_data = file.readlines()
    file.close()
    master_answer_key = list(map(str.strip,raw_data))    
    number_of_questions = master_answer_key[-1].split('-')[0]
    #print(master_answer_key)
    if(number_of_questions.isdigit()):
        number_of_questions = int(number_of_questions)
    else:
        print('Indexing of question numbers in the answer key is wrong,make sure question numbers are integers only as shown in the model answer key')
        sys.exit(0)
    max_sets = math.factorial(number_of_questions)
    number_of_sets = get_set_number(max_sets)    
    return master_answer_key,number_of_questions,number_of_sets
    
def AK_to_dictionary(answer_key):
    d_answer_key = {}
    for el in answer_key:
        d_answer_key[int(el.split('-')[0])] = el.split('-')[1]
    return d_answer_key


def get_question_paper_info():
    file  = open('QP.txt','r')
    raw_data = file.readlines()
    file.close()
    #print(raw_data)
    master_question_paper = list(map(str.strip,raw_data))
    #print(master_question_paper)
    d_question_paper = {}
    questions = [q for q in master_question_paper if q.startswith('Q')]
    
    for i in range(len(questions)-1):
        d_question_paper[questions[i]] = master_question_paper[master_question_paper.index(questions[i])+1:master_question_paper.index(questions[i+1])]
        if i==len(questions)-2:
            d_question_paper[questions[-1]] = master_question_paper[master_question_paper.index(questions[i+1])+1:]
    #print(d_question_paper)
    return d_question_paper

def eq(ch):
    return ord(ch)-96

def reveq(ch):
    return chr(ch+96)

def gen_valid_order(sets,noq):
    order = []
    while len(order) != noq:
        q = random.randint(1,noq)
        if q not in order:
            order.append(q)
    
    for s in sets:
        if order == sets[s][0]:
            return gen_valid_order(sets,noq)
    return order
   

def set_gen(master_question_paper,master_answer_key,number_of_questions,number_of_sets):
    master = {}
    for key in master_question_paper:
        master[key] = master_question_paper[key],master_answer_key[int(key.split('.')[0][1:])]
    #print(master)
    sets = {}

    #make the encrypted form of master in sets
    sets[1] = list(range(1,number_of_questions+1))
    
    all_options = []
    for key in master:
        op = master[key][0]
        options = []
        for el in op :
            if el == '':
                continue
            elif eq(el.split(')')[0])<0 or eq(el.split(')')[0])>26:
                print('Invalid character given for option, please refer to the readme.')
                sys.exit(0)
            else:
                options.append(eq(el.split(')')[0]))
        all_options.append(options)
    
    sets[1] = sets[1],all_options 
    #print(sets)
      
    #randomize questions

    for i in range(2,number_of_sets+1):
        new_set_questions = gen_valid_order(sets,number_of_questions)        
        new_set_options = []
        for q in new_set_questions:
            new_set_options.append(sets[1][1][q-1])
        sets[i] = new_set_questions,new_set_options
        #print(sets[i])
    
    #add list of answers to the sets

    for s in sets:
        sets[s] = sets[s],[eq(master_answer_key[x].split(')')[0]) for x in sets[s][0]]
        #print(sets[s])
    
    #randomize option order for each set

    for s in sets:
        if s!=1:
            all_new_options = []
            for q in sets[s][0][1]:
                new_options = []
                while len(new_options)!=len(q):
                    a = random.randint(min(q),max(q))
                    if a in new_options:
                        continue
                    else:
                        new_options.append(a)
                #print(new_options)
                all_new_options.append(new_options)
            sets[s] = sets[s][0][0],all_new_options,sets[s][1]
        else:
            sets[s] = sets[s][0][0],sets[s][0][1],sets[s][1]
    #print(sets)

    return sets


                  
def printer(sets,master_question_paper,number_of_questions):
    #print the questions papers and answer keys.
    for s in sets:
        file1 = open('QP Set - '+ str(s)+'.txt','w')
        file2 = open('AK Set - '+ str(s)+'.txt','w')
        for i in range(1,number_of_questions+1):
            question = ''
            options = ''
            for key in master_question_paper:
                if int(key.split('.')[0][1:]) == sets[s][0][i-1]:
                    question,options = key,master_question_paper[key]
                    #print(question,options)
                    file1.write('Q'+str(i)+'.'+'.'.join(key.split('.')[1:])+'\n')
                    count = 1
                    for op in sets[s][1][i-1]:
                        file1.write(reveq(count)+')'+')'.join(options[op-1].split(')')[1:])+'\n')
                        count+=1
                    file1.write('\n')
            file2.write(str(i)+'-'+reveq(sets[s][1][i-1].index(sets[s][2][i-1])+1)+')\n')

        

#extract information from the answer key

master_answer_key,number_of_questions,number_of_sets = get_answer_key_info()
master_answer_key = AK_to_dictionary(master_answer_key)

#extract information from the question paper
master_question_paper = get_question_paper_info()
#print(master_question_paper)


#generate the sets
sets = set_gen(master_question_paper,master_answer_key,number_of_questions,number_of_sets)

printer(sets,master_question_paper,number_of_questions)