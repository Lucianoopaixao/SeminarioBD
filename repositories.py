class MovieRepository:
    def __init__(self, driver):
        #conexão do banco 
        self.driver = driver

    def recomendar_colaborativo(self, nome_usuario):
        query = """
        MATCH (eu: Usuario {nome: $nome})-[:ASSISTIU]->(:Filme)<-[:ASSISTIU]-(parecido:Usuario)
        MATCH (parecido)-[:ASSISTIU]->(recomendado:Filme)
        WHERE NOT (eu)-[:ASSISTIU]->(recomendado)
        RETURN recomendado.titulo AS filme, count(DISTINCT parecido) AS usuarios_que_recomendam
        ORDER BY usuarios_que_recomendam DESC
        """
        
        with self.driver.session() as session:
            # Roda a query
            resultado = session.run(query, nome=nome_usuario)
            # Formata os dados de volta para uma lista do Python
            return [{"Filme": reg["filme"], "Pontos": reg["usuarios_que_recomendam"]} for reg in resultado]

    def recomendar_por_conteudo(self, nome_usuario):
        query = """
        MATCH (eu: Usuario {nome: $nome})-[:ASSISTIU]->(:Filme)-[:DO_GENERO]->(g:Genero)
        WITH eu, g, count(*) AS afinidade
        MATCH (sugestao: Filme)-[:DO_GENERO]->(g)
        WHERE NOT (eu)-[:ASSISTIU]->(sugestao)
        RETURN sugestao.titulo AS filme, sum(afinidade) AS pontuacao
        ORDER BY pontuacao DESC
        """
        with self.driver.session() as session:
            resultado = session.run(query, nome=nome_usuario)
            return [{"Filme": reg["filme"], "Pontos": reg["pontuacao"]} for reg in resultado]