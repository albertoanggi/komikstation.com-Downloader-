import requests
import shutil
from bs4 import BeautifulSoup as bs
import os

class KomikStationDownloader(object):

	def downloadFileWithURL(self,fileUrls,mangaTitle):
		if not os.path.exists(mangaTitle):
			os.makedirs(mangaTitle)
		for i, url in enumerate(fileUrls):
			r = requests.get(url, stream=True)
			if r.status_code == 200:
				with open('%s/%s.jpg' % (mangaTitle,i), 'wb') as f:
					shutil.copyfileobj(r.raw, f)
			else:
				raise Exception('Download file failure.')

	def getUrlImage(self, urlsChapterManga):
		for r in urlsChapterManga:
			urlsImage  = []
			page_data = requests.get(r)
			if page_data.status_code == 200:
				soup  = bs(page_data.content,'lxml')
				title = soup.select("div.headpost")[0].text.strip("\n").replace("/","-")
				image = soup.select("div#readerarea > img")
				for images in image:
					urlsImage.append(images.get("src"))
			else:
				return (page_data.status_code)
			self.downloadFileWithURL(urlsImage,title)

	def getUrlChapterManga(self,urlManga):
		urlsChapter = []
		page_data = requests.get(urlManga)
		if page_data.status_code == 200:
			soup = bs(page_data.content,'lxml')
			urlChapter = soup.select("ul > li > span.leftoff > a")
			for urls in urlChapter:
				urlsChapter.append(urls.get('href'))
		self.getUrlImage(urlsChapter)