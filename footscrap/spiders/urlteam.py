# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class UrlteamSpider(scrapy.Spider):
    name = 'urlteam'
    allowed_domains = ['www.transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/wettbewerbe/afrika']

    def delextrachar(self,str):
        delr = str.replace("\r", "")
        delt = delr.replace("\t", "")
        delv = delt.replace(",", "")
        final = delv.replace("\n", "")
        return final

    # def parse(self, response):
    #     urls = ['https://www.transfermarkt.com/wettbewerbe/europa',
    #             'https://www.transfermarkt.com/wettbewerbe/asien',
    #             'https://www.transfermarkt.com/wettbewerbe/amerika',
    #             'https://www.transfermarkt.com/wettbewerbe/afrika']
    #
    #     for url in urls:
    #
    #         yield Request(url, callback=self.parse_continent)

    def parse(self, response):
        urls = response.xpath('//*[@class="inline-table"]/tr/td/a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            print(url)
            yield Request(url, callback=self.parse_club)

    def parse_club(self, response):
        urls = response.xpath('//*[@class="hauptlink no-border-links show-for-small show-for-pad"]/a/@href').extract()
        for url in urls:
            urlcomplet = response.urljoin(url)
            yield Request(urlcomplet, callback=self.parse_joueurs)

    def parse_joueurs(self, response):
        defaut_link = 'https://www.transfermarkt.com/'
        urls = response.xpath('//*[@class="hide-for-small"]/a/@href').extract()
        for url in urls:
            sep_first_url = url.split('/')
            url = "/".join([sep_first_url[1],'leistungsdaten/spieler',sep_first_url[4],'/saison/ges/plus/1?saison=ges'])
            urlcomplet = defaut_link + url

            yield Request(urlcomplet, callback=self.parse_data)

    def parse_data(self, response):
        prenom = response.xpath('//*[@itemprop="name"]/text()').extract()
        nom = response.xpath('//*[@itemprop="name"]/b/text()').extract()
        age = response.xpath('//*[@itemprop="birthDate"]/text()').extract_first()
        nationalite = response.xpath('//*[@itemprop="nationality"]/text()').extract()
        team = response.xpath('//*[@itemprop="affiliation"]/a/text()').extract()
        dataItem = response.xpath('//*[@class="dataValue"]/text()').extract()
        competitions =  response.xpath('//*[@class="hauptlink no-border-rechts"]/img/@title').extract()
        stats = response.xpath('//*[@class="zentriert"]/text()').extract()[0:(len(competitions)+1)*11+1]
        ligue = response.xpath('//*[@class="mediumpunkt"]/a/text()').extract()

        try :
            poste1 = response.xpath('//*[@class="dataValue"][1]/text()').extract()[6]
            poste2 = response.xpath('//*[@class="dataValue"][1]/text()').extract()[3]
        except:
            poste1 = "NaN"
            poste2 = "NaN"

        try:
            buts_selection = response.xpath('//*[@class="dataValue"]/a/text()').extract()[-1]
            selections_nation = response.xpath('//*[@class="dataValue"]/a/text()').extract()[-2]
        except:
            buts_selection = 0
            selections_nation = 0

        finContrat = self.delextrachar(dataItem[len(dataItem)-1])
        price = response.xpath('//*[@class="dataMarktwert"]/a/text()').extract_first()
        price_range = response.xpath('//*[@class="waehrung"]/text()').extract_first()


        yield {"nom": nom,
               "prenom": prenom,
               'age': age,
               'nationalite' : nationalite,
               'poste1':  self.delextrachar(str(poste1)),
               'poste2':  self.delextrachar(str(poste2)),
               'ligue':  self.delextrachar(ligue[1]),
               'equipe' : team,
               'price' : price,
               'price_range' : price_range,
               'fin_contrat' : finContrat,
               'competitions' : competitions,
               'stats' : stats,
               'buts_selection' : buts_selection,
               'selections_nation' : selections_nation
               }


# https://www.transfermarkt.fr/moussa-doumbia/profil/spieler/316137
# https://www.transfermarkt.fr/gianluigi-buffon/leistungsdaten/spieler/5023/saison/2018/plus/1#gesamt
