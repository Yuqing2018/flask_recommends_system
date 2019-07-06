#!/usr/bin/python
# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import re
dbpedia_url = 'http://dbpedia.org/sparql'

def querySparql(query_str):
  sparql = SPARQLWrapper(dbpedia_url)
  sparql.setQuery(query_str)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  rs = results['results']['bindings']
  return rs

def getLang(keyword) :
    # 判断语言
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    m = re_words.search(keyword)
    if m != None:
        lang = 'zh'
    else:
        lang = 'en'
    return lang

# 搜索出版物
def queryPublications(keyword,type):
  lang = getLang(keyword)
  query_str = '''
  SELECT distinct ?pub ?name ?abstract ?pid 
  WHERE {
    ?pub rdf:type dbo:%s ;
         rdfs:label ?name ;
         dbo:abstract ?abstract ;
         dbo:wikiPageRevisionID ?pid .
    FILTER ( REGEX(?name, "%s", "i") && (LANG(?name)="%s") && (LANG(?abstract)="%s") ) .
}
ORDER BY DESC(?pid)
LIMIT 200
  ''' %(type, keyword, lang, lang)

  return querySparql(query_str)

# 查询出版物详细信息
def queryInfo(pid, type='Film', lang='en') :
  query_str = '''
  SELECT *
  WHERE {
  ?uri rdf:type dbo:%s ;
      dbo:wikiPageRevisionID ?pid ;
      rdfs:label ?name ;
      dbo:abstract ?abstract .
      FILTER ( (?pid=%s)&&(lang(?name)='%s')&&(lang(?abstract)='%s') )
  }
  LIMIT 1''' %(type, pid, lang, lang)

  return querySparql(query_str)

#相似出版物推荐
def recommend(pubname, pubtype) :
    # 替换括号
    patt = r'\(.*\)'
    pubname = re.sub(patt, '', pubname).replace(' ','_')
    query_str = '''
    SELECT COUNT(?pub) SAMPLE(?pub)
    WHERE {
	?res rdf:type dbo:%s ;
	     dct:subject ?o .
	?pub dct:subject ?o .
	FILTER ( REGEX(?res, "%s") && (?pub != ?res) ) .
} 
GROUP BY ?pub
ORDER BY DESC(count(?pub))
LIMIT 10
    '''%(pubtype, pubname)

    return querySparql(query_str)
