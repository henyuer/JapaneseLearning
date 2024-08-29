# 单词复习之平假名
import time
import argparse
import random
import os
import glob
import json


def text_color(text,color):
    if color=='red':
        return f"\033[31m{text}\033[0m"
    elif color=='green':
        return f"\033[32m{text}\033[0m"
    elif color=='yellow':
        return f"\033[33m{text}\033[0m"
    elif color=='blue':
        return f"\033[34m{text}\033[0m"
    else:
        return text

def main(file=None,reset=False,pseudonym='h'):
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
    
    if pseudonym=='h':
        print(text_color("平假名单词复习",'green'))
    elif pseudonym=='k':
        print(text_color("片假名单词复习",'green'))
    else:
        print(text_color("参数错误！",'red'))
        print(text_color("-p参数只能为h或k,默认为h",'green'))
        return

    # logic loop
    try:
        for idx in seq :
            chinese,dict_item=vocab_list[idx]
            if pseudonym=='h':
                japanese,w=list(dict_item.items())[0]
            else:
                try:
                    japanese,w=list(dict_item.items())[1]
                # if hiragana is same with katakana, it will be out of index.
                except IndexError:
                    japanese,w=list(dict_item.items())[0]
            w=2 if reset else w
            if w==0:
                continue
            chinese_output=chinese+":"
            user_iniput=input(f"\033[33m{chinese_output:<{fixed_length}}\033[0m")
            if japanese==user_iniput:
                correct+=1
                vocab[chinese][japanese]-=1
                print(text_color("you are right!",'blue'))
            else:
                vocab[chinese][japanese]+=2
                print(text_color(f"wrong! the answer is {japanese}",'red'))
                wrong_vocab[chinese]=japanese
            total+=1
    except KeyboardInterrupt:
        print(f"\n{text_color('单词复习中断！','red')}")


    # print result
    print(f"total word number: {total}, correct number: {correct}")
    print("correct rate:" + text_color(f"{correct/total*100}%",'green'))
    print(f"\nwrong words in this test are as follow:")
    for ch,ja in wrong_vocab.items():
        sentence=": "+ja
        print(text_color(f"  {ch:<{10}}{sentence}",'green'))

    # change weights to json file
    with open(file,'w',encoding='utf-8') as f:
        json.dump(vocab,f,ensure_ascii=False,indent=4)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--file',type=str,help="单词表路径")
    parser.add_argument('-r','--reset',action='store_true',help="重置单词权重")
    parser.add_argument('-p','--pseudonym',type=str,default='h',help="设置单词表的假名类型，h为平假名，k为片假名")

    args=parser.parse_args()
    main(file=args.file,reset=args.reset,pseudonym=args.pseudonym)