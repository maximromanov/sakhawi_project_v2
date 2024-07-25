import re

textPath = "../data/0902Sakhawi.DawLamic.ITO20230111-ara1.EIS1600"
uriBase  = "0902Sakhawi.DawLamic.ITO20230111-ara1.EIS1600"
reference = "<i>al-Ḍawʾ al-Lāmiʾ lī-Ahl al-Qarn al-Tāsiʿ</i>"


with open("template.html", "r") as f1:
    template = f1.read()
    #print(template)

bioPath = "../data/0902Sakhawi.DawLamic/"
stylePath = "../style.css"
lenName = 350

poetryTemplate2 = '<table class="poetryTable"><tr><td>%s</td><td>%s</td></tr></table>'
poetryTemplate1 = '<table class="poetryTable"><tr><td>%s</td></tr></table>'

def processText(text):
    # clean
    text = re.sub("ms\d+|\$|Page\w+", "", text)
    text = re.sub(r"(\w)\n(\w)", r"\1 \2", text)

    textL = text.split("\n")
    text = []
    for t in textL: 
        if "%~%" in t: # poetry
            t = re.sub("^%~%|%~%$", "", t.strip())
            ta = t.split("%~%")
            if len(ta) == 2:
                t = poetryTemplate2 % (ta[0], ta[1])
            elif len(ta) == 1:
                t = poetryTemplate1 % (ta[0])
            else:
                #print(ta)
                #input(t)
                t = poetryTemplate1 % (t)
            text.append(t)
        else: # regular paragraph
            t = '<p class="arabic prose">%s</p>' % t
            text.append(t)
    text = "\n\n".join(text)
    # fix poetry table :: '<table class="poetryTable"><tr><td>%s</td><td>%s</td></tr></table>'
    text = re.sub('</table>\n\n<table[^>]+>', "", text)
    # page numbers
    # headers
    return(text)


def generateData(textPath):
    prosop = []

    with open(textPath, "r") as f1:
        data = f1.read().replace("_ء_", "")
        data = re.split(r"\n#=(\d+)= ", data)

        realData = data[1:] # odd - ids; even - text
        print(len(realData))

        for i in range(0, len(realData), 2):
            ID = realData[i]
            text = realData[i+1]
            text = re.sub(r"\n=\d+.*\n", "\n\n", text)
            text = re.sub(r"BIO_\w+", "", text)


            if "$" in text:
                textFormatted = processText(text)

                final = template
                final = final.replace("#BIO#", ID)
                final = final.replace("STYLEPATH", stylePath)
                final = final.replace("FULLREFERENCE", reference)
                final = final.replace("PASSAGEURI", uriBase+"."+ID)
                final = final.replace("MAINHTMLTEXT", textFormatted)

                name = text.replace("$", "").replace("\n", " ").replace("  ", " ").strip()
                name = name.split(".")[0]
                #name = re.sub("[A-Za-z0-9]+", "", name).replace("  ", " ")
                name = re.sub(r"^[-=:~_ ]+", "", name)
                name = re.sub(r"Page\w+|ms\w+", " ", name)
                name = re.sub(r" +", " ", name)
                if len(name) > lenName:
                    name = name[:lenName] + "..."

                name = f"[{ID}] {name}"
                #input(name)

                prosop.append("%s\t%s" % (ID, name))

                # ADD HERE CODE TO REPLACE EMPTY IMAGES WITH ACTUAL GRAPHS
                # final = final.replace("MAINHTMLTEXT", textFormatted)

                with open(bioPath+ID+".html", "w") as f9:
                    f9.write(final)

        with open("../data/prosopData.tsv", "w") as f9:
            f9.write("ID\tNAME\n"+ "\n".join(prosop))

generateData(textPath)