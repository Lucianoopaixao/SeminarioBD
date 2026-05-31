from database import Neo4jConnection

def povoar_base_de_dados(driver):
    
    query_filmes = """
    UNWIND [
        {titulo:'As Vantagens de Ser Invisível', ano:2012, generos: ['Romance', 'Drama']},
        {titulo: 'Pecadores', ano:2025, generos: ['Terror', 'Ação']},
        {titulo: 'Parasita', ano:2019, generos: ['Thriller', 'Comédia']},
        {titulo: 'Vingadores', ano:2012, generos: ['Ação', 'Aventura']},
        {titulo: 'Pantera Negra', ano:2018, generos: ['Ação', 'Aventura']},
        {titulo:'O Senhor dos Anéis', ano:2001, generos: ['Fantasia', 'Aventura']},
        {titulo: 'Harry Potter', ano:2001, generos: ['Fantasia', 'Aventura']},
        {titulo: 'Toy Story', ano:1995, generos: ['Animação', 'Família']},
        {titulo: 'Procurando Nemo', ano:2003, generos: ['Animação', 'Família']},
        {titulo:'O Poderoso Chefão', ano:1972, generos: ['Drama','Crime']},
        {titulo: 'Pulp Fiction', ano:1994, generos: ['Crime', 'Drama']},
        {titulo: 'Conclave', ano:2024, generos: ['Thriller', 'Mistério']},
        {titulo:'Matilda', ano:1996, generos: ['Fantasia', 'Comédia']},
        {titulo:'A Noiva Cadáver', ano:2005, generos: ['Animação', 'Fantasia', 'Romance']},
        {titulo: 'Tartarugas Até Lá Embaixo', ano:2024, generos: ['Drama', 'Romance']},
        {titulo: 'Cidade de Deus', ano:2002, generos: ['Crime', 'Drama']},
        {titulo:'La La Land', ano:2016, generos: ['Romance', 'Musical', 'Drama']},
        {titulo: 'Mulherzinhas', ano:2019, generos: ['Drama', 'Romance']}
    ] AS f
    MERGE (filme:Filme {titulo: f.titulo})
    SET filme.ano = f.ano
    WITH filme, f
    UNWIND f.generos AS nomeGenero
    MERGE (g:Genero {nome: nomeGenero})
    MERGE (filme)-[:DO_GENERO]->(g)
    """

   
    query_usuarios = """
    UNWIND [
        {usuario: 'Luciano', titulo:'As Vantagens de Ser Invisível', nota:5},
        {usuario: 'Luciano', titulo:'A Noiva Cadáver', nota:4},
        {usuario: 'Luciano', titulo: 'Pecadores', nota:5},
        {usuario: 'Luciano', titulo: 'Parasita', nota:4},
        {usuario: 'Luciano', titulo: 'Vingadores', nota:4},
        {usuario: 'Bruno', titulo:'As Vantagens de Ser Invisível', nota:5},
        {usuario: 'Bruno', titulo:'A Noiva Cadáver', nota:5},
        {usuario: 'Bruno', titulo: 'Pecadores', nota:4},
        {usuario: 'Bruno', titulo: 'Vingadores', nota:5},
        {usuario: 'Bruno', titulo: 'Pantera Negra', nota:4},
        {usuario: 'Marcos', titulo: 'As Vantagens de Ser Invisível', nota:4},
        {usuario: 'Marcos', titulo: 'Parasita', nota:5},
        {usuario: 'Marcos', titulo: 'Pecadores', nota:4},
        {usuario: 'Marcos', titulo: 'Conclave', nota:4},
        {usuario: 'Marcos', titulo: 'Cidade de Deus', nota:5},
        {usuario: 'Clarissa', titulo: 'Pecadores', nota:4},
        {usuario: 'Clarissa', titulo: 'Parasita', nota:4},
        {usuario: 'Clarissa', titulo: 'As Vantagens de Ser Invisível', nota:5},
        {usuario: 'Clarissa', titulo: 'A Noiva Cadáver', nota:3},
        {usuario: 'Clarissa', titulo: 'Matilda', nota:4},
        {usuario: 'Clarissa', titulo: 'Mulherzinhas', nota:5},
        {usuario: 'Lavinya', titulo:'O Senhor dos Anéis', nota:5},
        {usuario: 'Lavinya', titulo: 'A Noiva Cadáver', nota:5},
        {usuario: 'Lavinya', titulo: 'Matilda', nota:5},
        {usuario: 'Lavinya', titulo: 'Tartarugas Até Lá Embaixo', nota:3},
        {usuario: 'Lavinya', titulo: 'Harry Potter', nota:5},
        {usuario: 'Lavinya', titulo: 'Toy Story', nota:3},
        {usuario: 'Jaiane', titulo: 'Harry Potter', nota:4},
        {usuario: 'Jaiane', titulo:'O Senhor dos Anéis', nota:4},
        {usuario: 'Jaiane', titulo: 'Procurando Nemo', nota:5},
        {usuario: 'Jaiane', titulo: 'Matilda', nota:4},
        {usuario: 'Ana Raquel', titulo:'O Poderoso Chefão', nota:5},
        {usuario: 'Ana Raquel', titulo:'Pulp Fiction', nota:5},
        {usuario: 'Ana Raquel', titulo:'Conclave', nota:4},
        {usuario: 'Ana Raquel', titulo:'Cidade de Deus', nota:5},
        {usuario: 'Elena', titulo:'Toy Story', nota:5},
        {usuario: 'Elena', titulo: 'Procurando Nemo', nota:5},
        {usuario: 'Elena', titulo: 'Harry Potter', nota:3},
        {usuario: 'Elena', titulo:'A Noiva Cadáver', nota:4},
        {usuario: 'Catarina', titulo: 'La La Land', nota:5},
        {usuario: 'Catarina', titulo: 'Mulherzinhas', nota:5},
        {usuario: 'Catarina', titulo:'As Vantagens de Ser Invisível', nota:4},
        {usuario: 'Catarina', titulo: 'Tartarugas Até Lá Embaixo', nota:4},
        {usuario: 'Leonardo', titulo: 'Cidade de Deus', nota:5},
        {usuario: 'Leonardo', titulo: 'O Poderoso Chefão', nota:4},
        {usuario: 'Leonardo', titulo: 'Pulp Fiction', nota:4},
        {usuario: 'Leonardo', titulo: 'Vingadores', nota:4},
        {usuario: 'Leonardo', titulo: 'La La Land', nota:3}
    ] AS r
    MERGE (u:Usuario {nome: r.usuario})
    WITH u, r
    MATCH (f:Filme {titulo: r.titulo})
    MERGE (u)-[a:ASSISTIU]->(f)
    SET a.nota = r.nota
    """

    with driver.session() as session:
        # limpa antes
        print("A limpar a base de dados...")
        session.run("MATCH (n) DETACH DELETE n")
        
        # inserção
        print("A inserir filmes e géneros...")
        session.run(query_filmes)
        
        #  notas e utilizadores
        print("A inserir utilizadores e notas...")
        session.run(query_usuarios)
        
        print("\nPovoamento concluído com sucesso! ✅ O ambiente está pronto para testes.")

if __name__ == "__main__":
    db = Neo4jConnection()
    try:
        povoar_base_de_dados(db.get_driver())
    except Exception as e:
        print(f"Erro ao povoar a base de dados: {e}")
    finally:
        db.close()