from database import Neo4jConnection
from repositories import MovieRepository

def main():
    print("Iniciando Sistema de Recomendação de Filmes...\n")
    
    # Instancia a conexão com o banco
    db = Neo4jConnection()
    
    try:
        
        repo = MovieRepository(db.get_driver())
        
        usuario_alvo = "Luciano" # nome pra teste
        
       
        print(f"--- Recomendações Colaborativas para {usuario_alvo} ---")
        recomendacoes_colab = repo.recomendar_colaborativo(usuario_alvo)
        
        for rec in recomendacoes_colab:
            print(f"Filme: {rec['Filme']} | Relevância: {rec['Pontos']}")
            
        print("\n----------------------------------------------------\n")
        
       
        print(f"--- Recomendações por Conteúdo para {usuario_alvo} ---")
        recomendacoes_conteudo = repo.recomendar_por_conteudo(usuario_alvo)
        
        for rec in recomendacoes_conteudo:
            print(f"Filme: {rec['Filme']} | Relevância: {rec['Pontos']}")

        print("\n----------------------------------------------------\n")


        print("--- Filmes mais bem avaliados (Nota Média) ---")
        filmes_top = repo.filmes_mais_bem_avaliados()
        for f in filmes_top:
            print(f"Filme: {f['Filme']} | Nota Média: {f['Nota_Media']} | Avaliações: {f['Qtd_Avaliacoes']}")

        print("\n----------------------------------------------------\n")

        usuario_vizinho = "Clarissa"
        print(f"--- Usuário mais parecido com a {usuario_vizinho} ---")
        vizinhos = repo.usuario_mais_parecido(usuario_vizinho)
        for v in vizinhos:
            filmes_comum = ", ".join(v['Quais']) 
            print(f"Usuário: {v['Usuario']} | Filmes em comum: {v['Filmes_Em_Comum']} | Quais: [{filmes_comum}]")

        print("\n----------------------------------------------------\n")

        print("--- Gêneros mais populares do catálogo ---")
        generos_pop = repo.generos_mais_populares()
        for g in generos_pop:
            print(f"Gênero: {g['Genero']} | Visualizações: {g['Visualizacoes']}")

    except Exception as e:
        print(f"Ocorreu um erro na aplicação: {e}")
        
    finally:
        
        db.close()
        print("\nConexão encerrada com sucesso.")

if __name__ == "__main__":
    main()