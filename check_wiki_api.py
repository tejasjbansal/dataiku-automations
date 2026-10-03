import dataikuapi, inspect
print(inspect.signature(dataikuapi.dss.wiki.DSSWiki.create_article))
print("---")
print(dataikuapi.dss.wiki.DSSWiki.create_article.__doc__ or "no docstring")
