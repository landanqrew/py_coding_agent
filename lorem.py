from loremipsum import Generator


if __name__ == "__main__":
    generator = Generator()
    for i in range(10):
        paragraph = generator.generate_paragraphs(5, True).send(None)[2]
        with open("calculator/lorem.txt", "a") as f:
            f.write(paragraph.replace("'", "") + "\n\n")