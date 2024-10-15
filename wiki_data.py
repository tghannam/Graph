G_list = [x for x in G.nodes()]
for node in G_list:
    try:
        
        site = pywikibot.Site("en", "wikipedia")
        title = wikipedia.page(node, auto_suggest=True).title
        page = pywikibot.Page(site, node)
        item = pywikibot.ItemPage.fromPage(page)
        item_dict = item.get()
        from wikidata.client import Client
        client = Client()  # doctest: +SKIP
        entity = client.get(item.id, load=True)
        string = entity.description.__str__()
        dates = re.findall('(\d{4})', string)
        G.add_node(node,  dob=dates[0], dod=dates[1])
        nationality = re.findall('([A-Z][-A-Za-z]+)(\s[A-Z][-A-Za-z]+)?', string)[0][0]
        G.add_node(node, nationality = nationality, person = 1, info = string)
    except:
        G.add_node(node, person= 0, nationality=0, info=string)
    if  G.nodes(data=True)[node]['person'] == 0:
        try:
            url = wikipedia.page(node).url
        except wikipedia.exceptions.DisambiguationError as e:
                                #leonardo_edges.append(x + '_ambiguity')
            continue
        except wikipedia.exceptions.PageError:
            continue
            
        try:
            infoboxes = read_html(url, index_col=0, attrs={"class":"infobox"}, )
            #wikitables = read_html(page, index_col=0, attrs={"class":"wikitable"})
            df = pd.DataFrame(infoboxes[0])
            if 'Born' in df.index:
                G.add_node(node, person= 1)
                try: 
                    born_text = ' '.join(re.split('(\d{4})', df.loc['Born'].values[0]))
                    born_date = re.findall('(\d{4})',born_text,)
                    died_text = ' '.join(re.split('(\d{4})', df.loc['Died'].values[0]))
                    died_date = re.findall('(\d{4})',died_text,)
                    G.add_node(node, dob=born_date[0], dod=died_date[0], info='NA')
                except:
                    continue
            else:
                G.add_node(node, person = 0, dob=0, dod=0)
                
            if 'Nationality' in df.index:
                G.add_node(node, nationality=df.loc['Nationality'].values[0])    
            else:
                G.add_node(node, nationality = 'NA')
        except:
            continue
