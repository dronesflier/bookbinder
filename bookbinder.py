import os

print("This script allows you to convert calibre's .epub files into a format that the Open Book understands.")



def main():
    os.system("rm outputbook.txt")
    os.system("rm -r /tmp/epubconverter")
    pathtoepub = input("Path to your .epub file: ")
    print("stripping .epub")
    stripspine(pathtoepub)
    os.system("touch outputbook.txt")
    contentopfparser()
    bookheader("outputbook.txt")
    bookbody("outputbook.txt")

def stripspine(epubpath):
    os.system("mkdir /tmp/epubconverter > /dev/null")
    os.system("cp " + epubpath + " /tmp/epubconverter/conversionbook.zip")
    os.system("unzip /tmp/epubconverter/conversionbook.zip -d /tmp/epubconverter > /dev/null")

def contentopfparser():
    global booktitle
    global bookauthor
    global bookdate
    global booklang
    contentfile = open("/tmp/epubconverter/content.opf", "r")
    contentfile = contentfile.read()
    contentfilelines = contentfile.splitlines() # so basically we want to split the lines of this file, and then figure the items and such out from there.
    for line in contentfilelines:
        if "dc:title" in str(line):
            #print("Titleline:" + line)
            booktitle = line.split("<dc:title>")[1].replace("</dc:title>", "")
        if "dc:creator" in str(line):
            #print("Creatorline:" + line)
            bookauthor = line.split("<dc:creator")[1].split(">")[1].replace("</dc:creator", "")
        if "dc:date" in str(line):
            #print("Dateline:" + line)
            bookdate = line.split("<dc:date>")[1].replace("</dc:date>", "")[:4]
        if "dc:language" in str(line):
            #print("LangLine:" + line)
            booklang = line.split("<dc:language>")[1].replace("</dc:language>", "")


def bookheader(path2book):
    print("Author: "+ bookauthor + ", Title: " + booktitle + ", Publishing date: " + bookdate + ", Language: " + booklang)
    bookfile = open(path2book, "a")
    bookfile.write("---\n") # This is the beginning of the Open Book file header.
    bookfile.write("AUTH: " + bookauthor + "\n")
    bookfile.write("TITL: " + booktitle + "\n")
    bookfile.write("YEAR: " + bookdate + "\n")
    bookfile.write("GNRE: Fiction\n")
    bookfile.write("LANG: " + booklang + "\n")
    bookfile.write("---\n")

def bookbody(path2book):
    bookfile = open(path2book, "a")
    # okay, this'll be interesting. I'll need to go into the text folder, iterate over all the "part*" files and ONLY
    # pull out <p class="calibre1"> stuff.
    # help.
    partfiles = os.listdir("/tmp/epubconverter/text")
    partfiles.sort()
    for part in partfiles:
        print("Parsing " + "/tmp/epubconverter/text/"+part)
        partfile = open("/tmp/epubconverter/text/"+part, "r")
        partfilelines = partfile.read().splitlines()
        for line in partfilelines:
            if 'p class="calibre1"' in str(line):
                if 'span data' in str(line):
                    print("span data :(")
                else:
                    # ok, great! Now we need to do bold and italic (mainly italic)
                    # libros uses  and  for shift out and shift in!
                    # italic
                    # bold
                    # italic and bold!
                    # yes, this is bullshit
                    # calibre seems to use <em class="calibre7"> for italic, not sure about bold ...
                    # i hope these ascii codes are correct btw, if not just swap em' round.
                    workingline = line.split('<p class="calibre1">')[1].replace("</p>", "")
                    if '</em>' in workingline:
                        workingline = workingline.replace('<em class="calibre7">', '')
                        workingline = workingline.replace('</em>', '')
                        fixedline = workingline
                    elif '</span>' in workingline: # this is a temporary fix for bold and italic crap
                        workingline = workingline.replace('<span class="sc">', '')
                        workingline = workingline.replace('</span>', '')
                        fixedline = workingline
                    else:
                        fixedline = workingline
                    bookfile.write(fixedline + "\n")

main()