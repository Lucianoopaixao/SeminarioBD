from database import Neo4jConnection
from repositories import MovieRepository

def main():
    print("Iniciando Sistema de Recomendação de Filmes...\n")
    
    # 1. Instancia a conexão com o banco
    db = Neo4jConnection()
    
    try:
        # 2. Instancia o repositório injetando a conexão do banco
        repo = MovieRepository(db.get_driver())
        
        usuario_alvo = "Luciano" # Substitua pelo nome que quiser testar
        
        # 3. Chama a função de recomendação colaborativa
        print(f"--- Recomendações Colaborativas para {usuario_alvo} ---")
        recomendacoes_colab = repo.recomendar_colaborativo(usuario_alvo)
        
        for rec in recomendacoes_colab:
            print(f"Filme: {rec['Filme']} | Relevância: {rec['Pontos']}")
            
        print("\n----------------------------------------------------\n")
        
        # 4. Chama a função de recomendação por conteúdo
        print(f"--- Recomendações por Conteúdo para {usuario_alvo} ---")
        recomendacoes_conteudo = repo.recomendar_por_conteudo(usuario_alvo)
        
        for rec in recomendacoes_conteudo:
            print(f"Filme: {rec['Filme']} | Relevância: {rec['Pontos']}")

    except Exception as e:
        print(f"Ocorreu um erro na aplicação: {e}")
        
    finally:
        # 5. Garante que o banco será fechado ao final do programa
        db.close()
        print("\nConexão encerrada com sucesso.")

if __name__ == "__main__":
    main()