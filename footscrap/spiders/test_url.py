urls = ['/moslem-haghshenas/profil/spieler/436130',
 '/saman-farjam/profil/spieler/607649',
 '/soroush-saeidi/profil/spieler/297933',
 '/mohammad-hossein-chegini/profil/spieler/612680',
 '/arash-zare/profil/spieler/609280',
 '/navid-zarnegar/profil/spieler/576579',
 '/seyed-abolfazl-ghoreishi/profil/spieler/336339',
 '/mehrdad-jamaati/profil/spieler/185517',
 '/kianoush-eghbali/profil/spieler/385304',
 '/hamid-sefid-gari/profil/spieler/476448',
 '/keykhosro-siahpour/profil/spieler/606155',
 '/omid-karimi/profil/spieler/603153',
 '/nima-bazoubandi/profil/spieler/644626',
 '/alireza-ghanbari/profil/spieler/646554',
 '/masoud-asadi/profil/spieler/603152',
 '/hamidreza-abdollahi/profil/spieler/608558',
 '/mohammad-javad-abbasi/profil/spieler/582676',
 '/mohammad-mehdi-zeynli/profil/spieler/612679',
 '/hamed-talebpour/profil/spieler/640551',
 '/arsalan-nekouhian/profil/spieler/612683',
 '/soheil-niknam/profil/spieler/436139',
 '/ali-hesami/profil/spieler/418418',
 '/alireza-lashkari/profil/spieler/582794',
 '/hamid-orangi/profil/spieler/478123',
 '/hadi-khadem/profil/spieler/476451',
 '/morteza-sanjanaki/profil/spieler/436129',
 '/mosadegh-deris/profil/spieler/605517',
 '/ali-mosallanejad/profil/spieler/389222',
 '/hossein-sadeghi/profil/spieler/455683',
 '/ali-azadmanesh/profil/spieler/582679',
 '/seyed-mohammad-mehri/profil/spieler/305523',
 '/ali-negarandeh/profil/spieler/476450',
 '/mostafa-nabati/profil/spieler/612681']

for url in urls :
    response = 'https://www.transfermarkt.fr'
    sep_first_url = url.split('/')

    url = "/".join([sep_first_url[1],'leistungsdaten/spieler',sep_first_url[4],'/saison/ges/plus/1#'])
    urlcomplet = response + url
    print(urlcomplet)
    # print(urlcomplet)
