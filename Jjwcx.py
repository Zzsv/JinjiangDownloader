import requests
from lxml import etree


class Downloader:
    """晋江小说下载器"""

    def __init__(self):
        self.book_url = input("Please type the url: ")
        try:
            self.book_r = requests.get(self.book_url)
        except:
            print("BOOK URL ERROR!")
            exit()
        else:
            print("Successfully get url: ", self.book_url)
        self.book_info = {
            "name": "",
            "author": "",
            "introduction": "",
        }

    def get_info(self):
        """获取书名，作者，介绍"""
        self.book_r.encoding = "gb18030"
        self.book_tree = etree.HTML(self.book_r.text)
        self.book_info["name"] = self.book_tree.xpath(
            '//*[@id="oneboolt"]/tbody/tr[1]/td/div/span/h1/span/text()'
        )[0]
        self.book_info["author"] = self.book_tree.xpath(
            '//*[@id="oneboolt"]/tbody/tr[1]/td/div/h2/a/span/text()'
        )[0]
        self.book_info["introduction"] = self.upper_format(
            self.book_tree.xpath('//div[@id="novelintro"]/text()')
        )
        print(self.book_info["introduction"])

    def get_chapter_urls(self):
        """获取所有章节的url"""
        self.chapter_urls = self.book_tree.xpath(
            '//*[@id="oneboolt"]/tbody/tr/td[2]/span/div[1]/a/@href'
        )  # 这里获取的是所有未被锁和非VIP的章节

    def save_book(self):
        """调用ChapterDownloader类，并存储小说"""
        try:
            book = open(
                "G:/output/"
                + self.book_info["name"]
                + " - "
                + self.book_info["author"]
                + ".txt",
                "w",
                encoding="utf-8",
            )
        except:
            print("File Error")
            print("Try to save with another Filename")
            book = open(
                "G:/output/" + "tmpname.txt",
                "w",
                encoding="utf-8",
            )
        else:
            pass

        info = (
            "书名："
            + self.book_info["name"]
            + "\n作者："
            + self.book_info["author"]
            + "\n介绍：\n"
            + self.book_info["introduction"]
            + "\n\n"
        )
        book.write(info)
        if self.if_title_sorted:
            for url in self.chapter_urls:
                output = self.download(url)
                text = (
                    output["title"]
                    + "\n\n"
                    + output["content"]
                    + "\n\n"
                    + output["words"]
                )
                text += "\n\n\n"
                book.write(text)
        else:
            i = 1
            for url in self.chapter_urls:
                output = self.download(url)
                text = (
                    "第"
                    + str(i)
                    + "章 "
                    + output["title"]
                    + "\n\n"
                    + output["content"]
                    + "\n\n"
                    + output["words"]
                )
                text += "\n\n\n"
                i += 1
                book.write(text)
        print("Mission Accomplished")

    def if_title(self):
        """判断标题是否是第……章的形式"""
        url = self.chapter_urls[0]
        test = self.download(url)
        if ("第" in test["title"] and "章" in test["title"]) or (
            "第" in test["title"] and "篇" in test["title"]
        ):
            self.if_title_sorted = 1
        else:
            self.if_title_sorted = 0

    def download(self, url):
        """获取一章的标题，内容，作者有话要说"""
        output = {
            "title": "",
            "content": "",
            "words": "",
        }
        chapter = requests.get(url)
        chapter.encoding = "gb18030"
        chapter_element = etree.HTML(chapter.text)
        title = self.lower_format(
            chapter_element.xpath(
                '//*[@id="oneboolt"]/tr[2]/td[1]/div/div[2]/h2/text()'
            )[0]
        )
        output["title"] = title
        print("Successfully get ", title)
        content = chapter_element.xpath('//*[@id="oneboolt"]/tr[2]/td[1]/div/text()')
        content = self.upper_format(content)
        output["content"] = content

        words = chapter_element.xpath(
            '//*[@id="oneboolt"]/tr[2]/td[1]/div/div[@class="readsmall"]/text()'
        )
        words = self.upper_format(words)
        output["words"] = words

        return output

    @staticmethod
    def upper_format(unformated_contents):
        """将数组中的字符串格式化，并返回字符串。返回的字符串有段首缩进"""
        formated_contents = ""
        for unformated_content in unformated_contents:
            text = unformated_content.strip()
            if text != "":
                formated_contents += "\u3000\u3000" + text + "\n"
        return formated_contents

    @staticmethod
    def lower_format(unformated_content):
        """将传入字符串格式化，返回无段首缩进的字符串"""
        return unformated_content.strip()


if __name__ == "__main__":
    Jjwxc = Downloader()
    Jjwxc.get_info()
    Jjwxc.get_chapter_urls()
    Jjwxc.if_title()
    Jjwxc.save_book()
