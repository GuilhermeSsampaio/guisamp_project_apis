# from docling.document_converter import DocumentConverter
# converter = DocumentConverter()

# sites_url = [
#     "https://www.tudogostoso.com.br/",
#     "https://www.receitasnestle.com.br/",
#     "https://www.panelinha.com.br/",
#     "https://cybercook.com.br/",
#     "https://receitas.globo.com/",
#     "https://anamariabraga.globo.com/receitas/",
#     "https://www.terra.com.br/vida-e-estilo/culinaria/",
#     "https://www.allrecipes.com/",
#     "https://www.foodnetwork.com/",
#     "https://www.bbcgoodfood.com/",
#     "https://www.seriouseats.com/",
#     "https://www.epicurious.com/",
#     "https://tasty.co/",
#     "https://www.jamieoliver.com/recipes/",
# ]
# avaible_sites=[]
# sites_403 = []

# for url in sites_url:
#     try: 
#         result = converter.convert(url)
#         docling_txt = result.document.export_to_markdown()
#         print(f"Processed {url} successfully.")
#         avaible_sites.append(url)
#     except Exception as e:
#         print(f"Failed to process {url}: {e}")
#         sites_403.append(url)
        
# print("Available sites:", avaible_sites)
# print("Sites with 403 errors:", sites_403)

# # Available sites:
# [
#     'https://www.receitasnestle.com.br/',
#     'https://www.panelinha.com.br/',
#     'https://cybercook.com.br/',
#     'https://receitas.globo.com/',
#     'https://anamariabraga.globo.com/receitas/',
#     'https://www.terra.com.br/vida-e-estilo/culinaria/',
#     'https://www.allrecipes.com/',
#     'https://www.bbcgoodfood.com/',
#     'https://www.seriouseats.com/',
#     'https://www.epicurious.com/',
#     'https://tasty.co/',
#     'https://www.jamieoliver.com/recipes/'
# ]

# # Sites with 403 errors:
# [
#     'https://www.tudogostoso.com.br/',
#     'https://www.foodnetwork.com/'
# ]