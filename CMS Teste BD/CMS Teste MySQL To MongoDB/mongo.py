import pymongo
from pymongo import MongoClient
from decimal import Decimal
from bson.decimal128 import Decimal128
import numpy as np



def convert_decimal(dict_item):
    # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
    # Embedded dictionaries and lists are called recursively.
    if dict_item is None: return None

    for k, v in list(dict_item.items()):
        if isinstance(v, dict):
            convert_decimal(v)
        elif isinstance(v, list):
            for l in v:
                convert_decimal(l)
        elif isinstance(v, Decimal):
            dict_item[k] = Decimal128(str(float(v)))  # Decimal128(str(v))

    return dict_item

def correct_encoding(dictionary):
    """Correct the encoding of python dictionaries so they can be encoded to mongodb
    inputs
    -------
    dictionary : dictionary instance to add as document
    output
    -------
    new : new dictionary with (hopefully) corrected encodings"""

    new = {}
    for key1, val1 in dictionary.items():
        # Nested dictionaries
        if isinstance(val1, dict):
            val1 = correct_encoding(val1)

        if isinstance(val1, np.bool_):
            val1 = bool(val1)

        if isinstance(val1, np.int64):
            val1 = int(val1)

        if isinstance(val1, np.float64):
            val1 = float(val1)

        new[key1] = val1

    return new

def get_client(mongo_uri: str) -> pymongo.MongoClient: 
    client = MongoClient(host=mongo_uri, serverSelectionTimeoutMS=1000)
    return client

def get_database(client: pymongo.MongoClient) -> pymongo.database.Database: 
    db = client["tamonabolsa"]
    return db

def get_collection_noticias(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.noticias
    return collection

def get_collection_usuarios(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios
    return collection

def get_collection_usuarios_config(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_config 
    return collection

def get_collection_usuarios_log(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_log 
    return collection

def get_collection_usuarios_apuracao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_apuracao 
    return collection

def get_collection_usuarios_apuracao_calculada(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_apuracao_calculada 
    return collection

def get_collection_usuarios_comentario(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario
    return collection

def get_collection_usuarios_comentario_reacao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_reacao
    return collection

def get_collection_usuarios_comentario_denuncia(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_denuncia
    return collection

def get_collection_usuarios_comentario_alerta(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_comentario_alerta
    return collection

def get_collection_usuarios_nota_corretagem(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_nota_corretagem
    return collection
    
def get_collection_usuarios_nota_corretagem_data(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_nota_corretagem_data
    return collection
    
def get_collection_usuarios_nota_corretagem_oper(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_nota_corretagem_oper
    return collection

def get_collection_usuarios_carteira_projecao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_carteira_projecao
    return collection
    
def get_collection_usuarios_carteira_projecao_item(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_carteira_projecao_item
    return collection

def get_collection_usuarios_cei(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_cei
    return collection
    
def get_collection_usuarios_cei_oper(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_cei_oper
    return collection
    
def get_collection_usuarios_cei_prov(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.usuarios_cei_prov
    return collection

def get_collection_empresa_setor(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_setor
    return collection

def get_collection_empresa_subsetor(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_subsetor
    return collection

def get_collection_empresa_segmento(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_segmento
    return collection

def get_collection_empresa(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa
    return collection

def get_collection_empresa_acao(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_acao
    return collection

def get_collection_empresa_fii(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_fii
    return collection

def get_collection_empresa_etf(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_etf
    return collection

def get_collection_empresa_bdr(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_bdr
    return collection

def get_collection_empresa_cripto(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_cripto
    return collection

def get_collection_empresa_finan(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan
    return collection

def get_collection_empresa_finan_agenda(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_agenda
    return collection

def get_collection_empresa_finan_bpa_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpa_tri
    return collection

def get_collection_empresa_finan_bpa_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpa_ano
    return collection

def get_collection_empresa_finan_bpp_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpp_tri
    return collection

def get_collection_empresa_finan_bpp_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_bpp_ano
    return collection

def get_collection_empresa_finan_dfc_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dfc_tri
    return collection

def get_collection_empresa_finan_dfc_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dfc_ano
    return collection

def get_collection_empresa_finan_dre_tri(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dre_tri
    return collection

def get_collection_empresa_finan_dre_ano(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_finan_dre_ano
    return collection

def get_collection_empresa_cotacoes(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.empresa_cotacoes
    return collection

def get_collection_admin_log_erros(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.admin_log_erros 
    return collection

def get_collection_admin_fatos(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.admin_fatos 
    return collection

def get_collection_xxxxxxxx(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    collection = db.xxxxxxxx
    return collection


