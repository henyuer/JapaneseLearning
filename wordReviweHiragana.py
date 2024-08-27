# 单词复习之平假名
import time
import argparse
import random
import os
import glob
import json



def main(file=None,reset=False):
    # if file is None
    # assign file with the newest json file in ./wordLists
    if file is None:
        json_file=glob.glob('.\\wordLists\\*.json')

        if json_file:
            json_file.sort(key=os.path.getatime,reverse=True)
            file=json_file[0]
        else:
            print("No JSON file found in .\\wordLists directory.")
            return
    else:
        file='.\\wordLists\\'+file
    print(file)
    
    # defination and pre operation
    with open(file,'r',encoding='utf-8') as f:
        vocab=json.load(f)
    vocab_list=list(vocab.items())
    seq=list(range(len(vocab)))
    random.seed(int(time.time()))
    random.shuffle(seq)
    total,correct=0,0
    fixed_length=10

    wrong_vocab={}
    
    print("平假名单词复习")

    # logic loop
    try:
        for idx in seq :
            chinese,dict_item=vocab_list[idx]
            japanese,w=list(dict_item.items())[0]
            w=3 if reset else w
            if w==0:
                continue
            total+=1
            chinese_output=chinese+":"
            user_iniput=input(f"\033[33m{chinese_output:<{fixed_length}}\033[0m")
            if japanese==user_iniput:
                correct+=1
                vocab[chinese][japanese]-=1
                print("\033[34myou are right!\033[0m")
            else:
                vocab[chinese][japanese]+=2
                print("\033[31myou are wrong!\033[0m")
                wrong_vocab[chinese]=japanese
    except KeyboardInterrupt:
        print("\n\033[31m单词复习中断！\033[0m")


    # print result
    print(f"total word number: {total}, correct number: {correct}")
    print(f"correct rate: {correct/total*100}%")
    print(f"\nwrong words in this test are as follow:")
    for ch,ja in wrong_vocab.items():
        sentence=": "+ja
        print(f"  \033[032m{ch:<{10}}{sentence}\033[0m")

    # change weights to json file
    with open(file,'w',encoding='utf-8') as f:
        json.dump(vocab,f,ensure_ascii=False,indent=4)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--file',type=str,help="单词表路径")
    parser.add_argument('-r','--reset',action='store_true',help="重置单词权重")

    args=parser.parse_args()
    main(file=args.file,reset=args.reset)