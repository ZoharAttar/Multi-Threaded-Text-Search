from threading import Thread
import math


def searchFunc(lines, StringToSearch, delta, n, partition):  # finding the string in the text
    '''

    :param lines: part of the text the specific thread search in
    :param StringToSearch: string we need to search in the text
    :param delta: space between the letters in the string we search
    :param n: the number of the thread we using right now
    :param partition: number of rows in each thread
    :return: printing the line number and the index of the string we searched in the text.in case of not found printing-
     'not found'
    '''

    fix_str = list(StringToSearch)
    len_str = len(fix_str)
    global find

    for index, line in enumerate(lines):  # going over the lines
        line_len = len(line)

        for chr in range(line_len):  # going over the letters in the line
            counter = 0
            if delta > line_len and len_str != 1:
                break
            if line[chr] == fix_str[counter]:  # checking if the letters match
                if len_str == 1:
                    print([n * partition + index, chr])
                    find = True
                    continue
                i = chr
                c = counter + 1
                while c < len_str and (
                        i + 1 + delta) < line_len and c < len_str:  # in case of a match, checking the other letters in the string
                    if line[i + 1 + delta] == fix_str[c]:
                        i = i + delta + 1
                        c = c + 1
                        if c == len_str:
                            find = True
                            print([n * partition + index, chr])
                            counter = 0
                            break
                    else:
                        break


def DistributedSearch(textfile, StringToSearch, nThreads, Delta):  # opening the file and creating the threads
    '''

    :param textfile: the input file to search
    :param StringToSearch: the string we want to search in the text
    :param nThreads: number of threads we need to use for the search
    :param Delta: space between the letters in the string we search
    :return: printing the line number and the index of the string we searched in the text.in case of not found printing-
     'not found'
    '''
    with open(textfile, "r", encoding='utf8') as file:
        rows = file.readlines()
    len_rows = len(rows)
    partition = math.ceil(len_rows / nThreads)
    rows_partition = []
    global find
    find = False

    i = 0
    while i < len_rows:  # spliting the lines betweem the threads
        rows_partition.append(rows[i:i + partition])
        i = i + partition

    if len(rows_partition) > nThreads:
        itr = nThreads
    else:
        itr = len(rows_partition)

    threads = []
    for n in range(itr):  # creating the threads
        t = Thread(target=searchFunc, args=(rows_partition[n], StringToSearch, Delta, n, partition,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    file.close()
    if not find:
        print("not found")


