import pymupdf

def main():
    print("Hello from pdf2chunks!")
    doc = pymupdf.open("./data/REV2_CDA_V04_02072024.pdf")
    out = open("./output/output.txt", "wb")
    for page in doc:
        print(page.get_textpage().extractJSON())
        print("========================")
        print("========================")
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()

if __name__ == "__main__":
    main()
