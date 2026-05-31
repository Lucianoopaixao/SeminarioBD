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

    except Exception as e:
        print(f"Ocorreu um erro na aplicação: {e}")
        
    finally:
        
        db.close()
        print("\nConexão encerrada com sucesso.")

if __name__ == "__main__":
    main()