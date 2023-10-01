import cx_Oracle

# Conectar ao banco de dados Oracle
conn = cx_Oracle.connect("RM96104/120903@oracle.fiap.com.br:1521/ORCL")

# Criar um cursor
cursor = conn.cursor()

# Recuperar resultados da consulta
for row in cursor.fetchall():
    nome, idade = row
    print(f"Nome: {nome}, Idade: {idade}")

# Fechar o cursor
cursor.close()

# Confirmar a transação (se aplicável)
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
