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
        
    def filmes_mais_bem_avaliados(self):
        query = """
        MATCH (:Usuario)-[a:ASSISTIU]->(f:Filme)
        RETURN f.titulo AS filme,
               round(avg(a.nota), 2) AS nota_media,
               count(*) AS qtd_avaliacoes
        ORDER BY nota_media DESC, qtd_avaliacoes DESC;
        """
        with self.driver.session() as session:
            resultados = session.run(query)
            return [{"Filme": reg["filme"], "Nota_Media": reg["nota_media"], "Qtd_Avaliacoes": reg["qtd_avaliacoes"]} for reg in resultados]

    def usuario_mais_parecido(self, nome_usuario):
        query = """
        MATCH (eu:Usuario {nome: $nome_usuario})-[:ASSISTIU]->(f:Filme)<-[:ASSISTIU]-(outro:Usuario)
        RETURN outro.nome AS usuario,
               count(f) AS filmes_em_comum,
               collect(f.titulo) AS quais
        ORDER BY filmes_em_comum DESC;
        """
        with self.driver.session() as session:
            resultados = session.run(query, nome_usuario=nome_usuario)
            return [{"Usuario": reg["usuario"], "Filmes_Em_Comum": reg["filmes_em_comum"], "Quais": reg["quais"]} for reg in resultados]

    def generos_mais_populares(self):
        query = """
        MATCH (:Usuario)-[:ASSISTIU]->(:Filme)-[:DO_GENERO]->(g:Genero)
        RETURN g.nome AS genero, count(*) AS visualizacoes
        ORDER BY visualizacoes DESC;
        """
        with self.driver.session() as session:
            resultados = session.run(query)
            return [{"Genero": reg["genero"], "Visualizacoes": reg["visualizacoes"]} for reg in resultados]